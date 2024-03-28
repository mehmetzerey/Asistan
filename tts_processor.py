# tts_processor.py

import os
import time
import threading
import queue
import pygame
from TTS.api import TTS
import torch


class TTSProcessor:
    def __init__(self, device=None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        self.playback_queue = queue.Queue()
        print(device)

    def tts_to_file(self, sentence, file_path):
        if sentence.strip():
            self.tts.tts_to_file(text=sentence,
                                 speaker_wav=r"C:\Users\DARK\Downloads\female.wav", language="tr",
                                 file_path=file_path)
            self.playback_queue.put(file_path)

    def worker(self, sentences, done_event):
        for sentence in sentences:
            filename = f"sentence_{threading.get_ident()}_{int(time.time())}.wav"
            self.tts_to_file(sentence, filename)
        done_event.set()

    def playback_worker(self, done_event):
        pygame.mixer.init()
        while not done_event.is_set() or not self.playback_queue.empty():
            file_path = self.playback_queue.get()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.music.unload()
            os.remove(file_path)
            self.playback_queue.task_done()

    def text_to_speech_in_parallel(self, sentences):
        done_event = threading.Event()
        threading.Thread(target=self.worker, args=(sentences, done_event)).start()
        threading.Thread(target=self.playback_worker, args=(done_event,)).start()

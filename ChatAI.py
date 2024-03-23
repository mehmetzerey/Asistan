import os
import re
import time
import threading
import queue
import pygame
from openai import OpenAI
import Repository
from TTS.api import TTS
import speech_recognition as sr
import torch

# OPENAI_API_KEY ortam değişkeniyle ayarlanmalıdır
api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# CUDA cihazını kontrol et
device = "cuda" if torch.cuda.is_available() else "cpu"

print(device)

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Oynatma kuyruğu
playback_queue = queue.Queue()


def send_message(message):
    new_prompt = Repository.create_instruction_based_on_query(message)
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": new_prompt}],
        max_tokens=250
    )
    Repository.save_conversation(message, completion.choices[0].message.content)
    return completion.choices[0].message.content


def tts_to_file(sentence, file_path):
    if sentence.strip():
        tts.tts_to_file(text=sentence,
                        speaker_wav=r"C:\Users\DARK\Downloads\female.wav", language="tr",
                        file_path=file_path)
        playback_queue.put(file_path)  # Dosya yolu oynatma kuyruğuna eklenir


def worker(sentences, done_event):
    for sentence in sentences:
        filename = f"sentence_{threading.get_ident()}_{int(time.time())}.wav"
        tts_to_file(sentence, filename)
    done_event.set()  # İşlem tamamlandığında olayı ayarla


def playback_worker(done_event):
    pygame.mixer.init()
    while not done_event.is_set() or not playback_queue.empty():
        file_path = playback_queue.get()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Ses dosyası oynatılırken bekle
            time.sleep(0.1)
        pygame.mixer.music.unload()
        os.remove(file_path)
        playback_queue.task_done()


def text_to_speech_in_parallel(sentences):
    done_event = threading.Event()  # İşlemin tamamlandığını belirten olay
    threading.Thread(target=worker, args=(sentences, done_event)).start()
    threading.Thread(target=playback_worker, args=(done_event,)).start()


def process_text(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    text_to_speech_in_parallel(sentences)


def listen_and_transcribe():
    r = sr.Recognizer()
    r.pause_threshold = 0.5
    with sr.Microphone() as source:
        print("Lütfen konuşun...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language='tr-TR')
        print("Söylediğiniz: " + text)
        return text
    except sr.UnknownValueError:
        print("Google Web Speech API sesi anlayamadı.")
        return None
    except sr.RequestError as e:
        print(f"Google Web Speech API'den talep yapılırken bir hata oluştu; {e}")
        return None


def main():
    while True:
        user_input = input("Konuşmak için enter basın (Çıkmak için 'q' veya mikrofon için m yazın): ")
        if user_input.lower() == 'q':
            print("Görüşmek üzere!")
            break

        if user_input.lower() == 'm':
            text = listen_and_transcribe()
            if text is None:
                continue
            else:
                assistant_response = send_message(text)
                process_text(assistant_response)
        else:
            assistant_response = send_message(user_input)
            process_text(assistant_response)

if __name__ == "__main__":
    main()

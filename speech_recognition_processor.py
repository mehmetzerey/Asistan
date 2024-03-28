# speech_recognition_processor.py

import speech_recognition as sr


class SpeechRecognitionProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.pause_threshold = 0.5

    def listen_and_transcribe(self):
        with sr.Microphone() as source:
            print("Lütfen konuşun...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language='tr-TR')
            print("Söylediğiniz: " + text)
            return text
        except sr.UnknownValueError:
            print("Google Web Speech API sesi anlayamadı.")
            return None
        except sr.RequestError as e:
            print(f"Google Web Speech API'den talep yapılırken bir hata oluştu; {e}")
            return None

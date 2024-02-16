import os
from openai import OpenAI
import ChromaDbExapmles
from gtts import gTTS
import pygame
import re
import os
import time
from pydub import AudioSegment
import speech_recognition as sr

api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(
  api_key=api_key
)


def send_message(message):
    new_prompt = ChromaDbExapmles.create_instruction_based_on_query(message)

    # print(new_prompt)
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": new_prompt},
        ],
        max_tokens=250
    )
    print("prompt harcanan token:", completion.usage.prompt_tokens)
    print("asistanın harcadığı token:", completion.usage.completion_tokens)
    print("Toplam harcanan token:", completion.usage.total_tokens)
    print(completion.choices[0].message.content)
    ChromaDbExapmles.save_conversation(message, completion.choices[0].message.content)

    return completion.choices[0].message.content


def text_to_speech_and_play(sentences, speed=1.25):
    pygame.mixer.init()  # pygame mixer başlat
    files_to_delete = []  # Silinecek dosyaların listesi

    for i, sentence in enumerate(sentences):
        if sentence.strip():  # Boş cümleleri atla
            # Dosya adını belirle
            filename = f"sentence_{i}.mp3"
            temp_filename = f"temp_{i}.mp3"  # Hızlandırılmış ses için geçici dosya adı
            files_to_delete.extend([filename, temp_filename])  # Temizleme listesine ekle

            tts = gTTS(text=sentence, lang='tr')
            tts.save(filename)  # Ses dosyasını kaydet

            # Pydub ile ses dosyasını yükle ve hızını ayarla
            sound = AudioSegment.from_file(filename)
            playback_speed = sound.speedup(playback_speed=speed)
            playback_speed.export(temp_filename, format="mp3")  # Hızlandırılmış dosyayı kaydet

            # pygame ile hızlandırılmış ses dosyasını oynat
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # Oynatma bitene kadar bekle
                time.sleep(0.1)

            pygame.mixer.music.stop()  # Oynatma bittiğinde müziği durdur
            pygame.mixer.music.unload()  # Kaynağı serbest bırak

    # Oynatma ve kaynak serbest bırakma işlemi bittikten sonra dosyaları sil
    for filename in files_to_delete:
        os.remove(filename)


def process_text(text):
    # Metni cümlelere ayır
    sentences = re.split(r'(?<=[.!?]) +', text)
    text_to_speech_and_play(sentences)


def listen_and_transcribe():
    # Ses tanıma nesnesi oluştur
    r = sr.Recognizer()

    # Mikrofonu varsayılan sistem mikrofonu olarak kullan
    with sr.Microphone() as source:
        print("Lütfen konuşun...")
        # Gürültüyü azaltmak için mikrofonu ayarla
        r.adjust_for_ambient_noise(source)
        # Kullanıcıdan sesi al
        audio = r.listen(source)

    # Google Web Speech API kullanarak sesi tanıma ve yazıya dönüştürme
    try:
        # 'tr-TR' Türkçe dil desteği için
        text = r.recognize_google(audio, language='tr-TR')
        print("Söylediğiniz: " + text)
        return text
    except sr.UnknownValueError:
        print("Google Web Speech API sesi anlayamadı.")
        return None
    except sr.RequestError as e:
        print(f"Google Web Speech API'den talep yapılırken bir hata oluştu; {e}")
        return None


while True:
    user_input = input("konuşmak için enter basın (Çıkmak için 'q' yazın): ")
    if user_input.lower() == 'q':
        print("Görüşmek üzere!")
        break

    text = listen_and_transcribe()
    if text is None:
        continue
    else:
        asistant_response = send_message(text)
        sentences = re.split(r'(?<=[.!?]) +', asistant_response)
        text_to_speech_and_play(sentences)

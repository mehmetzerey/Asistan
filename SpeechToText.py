import speech_recognition as sr

# Ses tanıma nesnesi oluştur
recognize = sr.Recognizer()

# Mikrofonu varsayılan sistem mikrofonu olarak kullan
with sr.Microphone() as source:
    print("Lütfen konuşun...")
    # Gürültüyü azaltmak için mikrofonu ayarla
    recognize.adjust_for_ambient_noise(source)
    # Kullanıcıdan sesi al
    audio = recognize.listen(source)

# Google Web Speech API kullanarak sesi tanıma ve yazıya dönüştürme
try:
    # 'tr-TR' Türkçe dil desteği için
    print("Söylediğiniz: " + recognize.recognize_google(audio, language='tr-TR'))
except sr.UnknownValueError:
    print("Google Web Speech API sesi anlayamadı.")
except sr.RequestError as e:
    print(f"Google Web Speech API'den talep yapılırken bir hata oluştu; {e}")

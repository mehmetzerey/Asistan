# main.py

from chatgpt_client import ChatGPTClient
from gemini_client import GeminiClient
from tts_processor import TTSProcessor
from speech_recognition_processor import SpeechRecognitionProcessor


def main():
    # chat_client = ChatGPTClient()
    chat_client = GeminiClient()
    tts_processor = TTSProcessor()
    speech_processor = SpeechRecognitionProcessor()

    while True:
        user_input = input("Konuşmak için enter basın (Çıkmak için 'q' veya mikrofon için 'm' yazın): ")
        if user_input.lower() == 'q':
            print("Görüşmek üzere!")
            break

        if user_input.lower() == 'm':
            text = speech_processor.listen_and_transcribe()
            if text is None:
                continue
            else:
                assistant_response = chat_client.send_message(text)
                sentences = assistant_response.split('. ')
                tts_processor.text_to_speech_in_parallel(sentences)
        else:
            assistant_response = chat_client.send_message(user_input)
            sentences = assistant_response.split('. ')
            tts_processor.text_to_speech_in_parallel(sentences)


if __name__ == "__main__":
    main()

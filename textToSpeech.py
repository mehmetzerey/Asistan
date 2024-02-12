import os
from pathlib import Path
from openai import OpenAI

api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(
  api_key=api_key
)

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="onyx",
  input="Heeeyy ahmet nasılsın adamım işten geldin biliyorum yorgunsun sıkıntı yok toparlarız."
)

response.stream_to_file(speech_file_path)
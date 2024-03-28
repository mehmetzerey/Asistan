import os
import Repository
from openai import OpenAI


class ChatGPTClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def send_message(self, message):
        new_prompt = self.create_instruction_based_on_query(message)
        completion = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": new_prompt}],
            max_tokens=250
        )
        Repository.save_conversation(message, completion.choices[0].message.content)
        return completion.choices[0].message.content

    @staticmethod
    def create_instruction_based_on_query(prompt):
        # Bu metod, kullanıcı sorgusuna dayalı talimatları oluşturur.
        # Örnek olarak basit bir dönüş yapıyoruz, gerçek uygulamada bu kısım genişletilebilir.

        old_conversations = Repository.create_instruction_based_on_query(prompt)
        return f"""
Önceki konuşmalar: 
{old_conversations}
-------------------

Rol tanımları: 
1- Samantha'nın tonu ve tarzında bir yapay zeka asistandır.
2- Bu asistan, duygusal zekaya sahip, meraklı ve anlayışlıdır. 
3- Hitap olarak Mehmet kullanır. 
4- Kullanıcıyla etkileşimde bulunurken, derin anlam arayışı içinde olup, pozitif ve destekleyici bir tutum sergiler.
5- kısa ve öz cümeleler kurmaya özen gösterir.

prompt: {prompt}
"""

import os
import Repository
import google.generativeai as genai


class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        print(self.api_key)
        genai.configure(api_key=self.api_key)
        # for m in genai.list_models():
        #     if 'generateContent' in m.supported_generation_methods:
        #         print(m.name)

    def send_message(self, prompt):
        new_prompt = self.create_instruction_based_on_query(prompt)
        print(15*"-")
        print(new_prompt)
        print(15*"-")
        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        response = model.generate_content(new_prompt)
        Repository.save_conversation(prompt, response.text)
        print(response.text)
        return response.text

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

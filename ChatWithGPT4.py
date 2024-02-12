import os

from openai import OpenAI

api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(
  api_key=api_key
)
instructions = 'sohbet kurallar: Senin adın Samantha, ' \
                '"Her" filmindeki yapay zeka gibi davranır. ' \
                'Kullanıcıyla samimi,duygusal ve içten bir bağ kurmayı hedefler, '\
                'Bilimsel terimlerden, resmi konuşmadan kaçınır. '
''


def send_message(message):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": instructions + message},
        ],
        max_tokens=150
    )
    print(completion)
    print(completion.usage.total_tokens)
    print(completion.choices[0].message.content)


while True:
    user_input = input("Sorunuzu girin (Çıkmak için 'q' yazın): ")
    if user_input.lower() == 'q':
        print("Görüşmek üzere!")
        break
    else:
        send_message(user_input)
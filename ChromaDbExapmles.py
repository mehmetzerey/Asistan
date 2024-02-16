import chromadb
from datetime import datetime

chroma_client = chromadb.Client()

client = chromadb.PersistentClient(path="chromaData")
collection = client.get_or_create_collection(name="Conversations")
print(collection.count())


def save_conversation(prompt, assistant_response):
    timestamp = datetime.now().isoformat()
    collection.add(
        documents=["user: " + prompt + "\nasistant: " + assistant_response],
        metadatas=[{"type": "conversations", "timestamp": timestamp}],
        ids=[f"conversations_{timestamp}"]
    )


def create_instruction_based_on_query(query_text, max_results=5):
    # Sorgu sonucunu getir
    results = collection.query(
        query_texts=[query_text],
        n_results=max_results
    )

    # Bulunan sonuçlardan önceki konuşmaları birleştir
    old_conversations = ""
    for doc in results['documents']:
        if len(doc) > 0:  # Eğer doküman en az bir öge içeriyorsa
            old_conversations += f"\n{doc[0]} \n"
        else:
            old_conversations += "\n"  # Boş dokümanlar için placeholder

    # Yeni prompt oluştur
    new_prompt = f"""
Önceki konuşmalar: {old_conversations}
---

Samantha'nın tonu ve tarzında bir yapay zeka asistanı olarak, [{query_text}]. 
Bu asistan, duygusal zekaya sahip, meraklı ve anlayışlıdır. Hitap olarak Mehmet kullanır. 
Kullanıcıyla etkileşimde bulunurken, derin anlam arayışı içinde olup, pozitif ve destekleyici bir tutum sergiler.
Kısa ve öz cümeleler kurmaya özen gösterir"""
    print(new_prompt)
    return new_prompt
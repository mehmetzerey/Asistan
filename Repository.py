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
    # Önce son beş mesajı getir
    recent_results = collection.query(
        query_texts=[""],
        n_results=5  # Son 5 mesaj
    )

    # Sorgu sonucunu getir (sorgu metni varsa)
    query_results = collection.query(
        query_texts=[query_text] if query_text else [""],
        n_results=max_results
    )

    # Sonuçları birleştir
    documents = recent_results['documents'] + query_results['documents']

    # Tekrar eden dokümanları kaldırmak için bir yöntem
    seen = set()
    unique_documents = []
    for doc in documents:
        # Listeler hashlenebilir değil, bu yüzden tuple'a çeviriyoruz
        tuple_doc = tuple(doc)
        if tuple_doc not in seen:
            seen.add(tuple_doc)
            unique_documents.append(doc)

    # Bulunan sonuçlardan önceki konuşmaları birleştir
    old_conversations = ""
    for doc in unique_documents:
        if doc:  # Eğer doküman boş değilse
            old_conversations += f"\n{' '.join(doc)} \n"
        else:
            old_conversations += "\n"  # Boş dokümanlar için placeholder

    # Yeni prompt oluştur
    new_prompt = f"""
Önceki konuşmalar: 
{old_conversations}
---

Rol: Samantha'nın tonu ve tarzında bir yapay zeka asistandır.
Bu asistan, duygusal zekaya sahip, meraklı ve anlayışlıdır. Hitap olarak Mehmet kullanır. 
Kullanıcıyla etkileşimde bulunurken, derin anlam arayışı içinde olup, pozitif ve destekleyici bir tutum sergiler.
En kısa ve öz cümeleler kurmaya özen gösterir.

prompt: [{query_text}]
"""
    print(new_prompt)
    return new_prompt

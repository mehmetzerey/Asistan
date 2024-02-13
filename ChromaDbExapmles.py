import chromadb
from datetime import datetime

chroma_client = chromadb.Client()

client = chromadb.PersistentClient(path="chromaData")
collection = client.get_or_create_collection(name="Conversations")
print(collection.count())

def save_conversation(prompt, assistant_response):
    timestamp = datetime.now().isoformat()
    collection.add(
        documents=[prompt, assistant_response],
        metadatas=[{"type": "user_prompt", "timestamp": timestamp},
                   {"type": "assistant_response", "timestamp": timestamp}],
        ids=[f"prompt_{timestamp}", f"response_{timestamp}"]
    )

    print(collection.count())

    results = collection.query(
        query_texts=["proje üstünde çalışıyorum"],
        n_results=2
    )
    print("bulunan sonuçlar:", results)


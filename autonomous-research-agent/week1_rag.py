import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="research_docs")

documents = [
    "Apple reported revenue of $124 billion in Q1 2025, driven by iPhone sales.",
    "Apple's services division grew 20% year over year in Q1 2025.",
    "Apple CEO Tim Cook announced new AI features coming to iPhone in 2025."
]
collection.add(
    documents=documents,
    ids=["doc1", "doc2", "doc3"]
)
results = collection.query(
    query_texts=["What were Apple's Q1 2025 earnings?"],
    n_results=2
)

print(results)

retrieved_docs = results["documents"][0]
context = "\n".join(retrieved_docs)


messages = [
    {"role": "system", "content": "You are a helpful research assistant. Be concise."},
    {"role": "user", "content": f"Context: {context}\n\nQuestion: What was Apple's revenue in Q1 2025?"}
]

final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

print(final_response.choices[0].message)
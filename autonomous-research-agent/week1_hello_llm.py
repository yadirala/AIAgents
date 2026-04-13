from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)

messages = [
    {"role": "system", "content": "You are a helpful research assistant. Be concise."},
    {"role": "user", "content": "What is RAG in 2 sentences?"}
]
response = client.chat.completions.create(messages=messages, model="gpt-4o-mini")
print(response.choices[0].message.content)
print(response.usage.total_tokens)
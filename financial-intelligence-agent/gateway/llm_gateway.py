from dotenv import load_dotenv
import litellm
load_dotenv()


def call_llm(messages,model = "gpt-4o-mini"):
    response = litellm.completion(
        model=model,
        messages=messages,
        fallbacks=["gemini/gemini-1.5-flash", "groq/llama3-8b-8192"]
    )
    return response.choices[0].message.content

from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)

def get_weather(city):
    return f"The weather in {city} is sunny and 75°F"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "the city to get weather for"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

messages = [
    {"role": "system", "content": "You are a helpful research assistant. Be concise."},
    {"role": "user", "content": "What is the weather in Tokyo?"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools= tools,
    tool_choice="auto"
)
available_tools = {
    "get_weather": get_weather
}

tool_call = response.choices[0].message.tool_calls[0]
tool_name = tool_call.function.name
tool_args = json.loads(tool_call.function.arguments)
city = tool_args["city"]
function_to_call = available_tools[tool_name]
result = function_to_call(**tool_args)

print(response.choices[0].message)
print(result)

messages.append(response.choices[0].message)
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": result
})

final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

print(final_response.choices[0].message)
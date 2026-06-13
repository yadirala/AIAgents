import time
import litellm
from dotenv import load_dotenv
load_dotenv()

_metrics = {}  # module level store

def track_agent(agent_name, messages, model="gpt-4o-mini"):
    start_time = time.time()
    response = litellm.completion(
        model=model,    
        messages=messages,
        fallbacks=["gemini/gemini-1.5-flash", "groq/llama3-8b-8192"]
    )
    latency = time.time() - start_time
    tokens = response.usage.total_tokens
    cost = calculate_cost(model, response.usage.prompt_tokens, response.usage.completion_tokens)
    
    if agent_name not in _metrics:
        _metrics[agent_name] = {"calls": 0, "tokens": 0, "cost": 0.0, "latency": 0.0}
    _metrics[agent_name]["calls"] += 1
    _metrics[agent_name]["tokens"] += tokens
    _metrics[agent_name]["cost"] += cost
    _metrics[agent_name]["latency"] += latency
    return response.choices[0].message.content

def calculate_cost(model, prompt_tokens, completion_tokens):
    if "gpt-4o-mini" in model:
        input_cost = (prompt_tokens / 1_000_000) * 0.15
        output_cost = (completion_tokens / 1_000_000) * 0.60
        return input_cost + output_cost
    return 0.0

def get_metrics():
    return _metrics

def print_metrics():
    for agent, stats in _metrics.items():
        print(f"Agent: {agent}")
        print(f"  Calls: {stats['calls']}")
        print(f"  Tokens: {stats['tokens']}")
        print(f"  Cost: ${stats['cost']:.4f}")
        print(f"  Latency: {stats['latency']:.2f} seconds")

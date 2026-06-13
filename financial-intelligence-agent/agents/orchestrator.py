import json
import re
from langgraph.types import Send
from gateway.llm_gateway import call_llm
from metrics.tracker import track_agent

def orchestrator(state):
    company = state["company"]
    question = state["question"]
    
    agent_descriptions = {
        "news_fetcher": "Fetches latest news. Use when question involves current events, recent news, or market sentiment.",
        "sec_agent": "Analyzes SEC 10-K filing. Use when question involves risk factors, financial data, or regulatory issues."
    }
    
    agent_list_str = "\n".join([f"{name}: {desc}" for name, desc in agent_descriptions.items()])
    
    prompt = f"""The user asked: '{question}' about {company}.

Available agents:
{agent_list_str}

Return a JSON list of agent names to run. Example: ["news_fetcher"] or ["news_fetcher", "sec_agent"]
Return ONLY the JSON list, no other text."""
    
    response = track_agent("orchestrator", [
        {"role": "system", "content": "You are an orchestrator. Return ONLY a valid JSON list of agent names."},
        {"role": "user", "content": prompt}
    ])
    
    try:
        agents_to_run = json.loads(response)
    except json.JSONDecodeError:
        match = re.search(r'\[.*\]', response, re.DOTALL)
        if match:
            agents_to_run = json.loads(match.group())
        else:
            agents_to_run = ["news_fetcher", "sec_agent"]
    
    return [Send(agent, state) for agent in agents_to_run]
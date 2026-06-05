import json
import re
from gateway.llm_gateway import call_llm

def orchestrator(state):
    company = state["company"]
    question = state["question"]
    
    agent_descriptions = {
        "news_fetcher": "Fetches and summarizes the latest news articles about the company.",
        "sec_agent": "Analyzes the company's SEC filings to extract relevant information.",
        "sentiment_agent": "Determines the overall sentiment towards the company based on news and SEC analysis.",
        "risk_scorer": "Assigns a risk score to the company based on all available information.",
        "report_writer": "Writes a final report summarizing the analysis and answering the user's question."
    }
    
    agent_list_str = "\n".join([f"{name}: {desc}" for name, desc in agent_descriptions.items()])
    
    prompt = f"You are an orchestrator for financial analysis. The user has asked: '{question}' about {company}. Based on the following available agents:\n\n{agent_list_str}\n\nWhich agents should be run to answer the user's question? Return a JSON list of agent names that should be executed in order."
    
    response = call_llm([
        {"role": "system", "content": "You are an orchestrator that decides which agents to run based on the user's question and available agents."},
        {"role": "user", "content": prompt}
    ])
    
    # Parse response as JSON list
    try:
        agents_to_run = json.loads(response)
    except json.JSONDecodeError:
        match = re.search(r'\[.*\]', response, re.DOTALL)
        if match:
            agents_to_run = json.loads(match.group())
        else:
            agents_to_run = ["news_fetcher", "sec_agent", "sentiment_agent", "risk_scorer", "report_writer"]
    
    return {"agents_to_run": agents_to_run}

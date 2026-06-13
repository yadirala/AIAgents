from gateway.llm_gateway import call_llm
from metrics.tracker import track_agent

def risk_scorer(state):
    news_summary = state["news_summary"]
    sec_summary = state["sec_summary"]
    sentiment = state["sentiment"]
    completed_agents = state.get("completed_agents", [])
    combined_input = f"News Summary: {news_summary}\n\nSEC Summary: {sec_summary}\n\nSentiment Analysis: {sentiment}\n\nBased on the above..."
    
    risk_score = track_agent("risk_scorer", [
        {"role": "system", "content": "You are a financial analyst. Based on the news summary and SEC summary, determine a risk score for the company. Be concise and focus on key risks and mitigating factors."},
        {"role": "user", "content": combined_input}
    ])
    completed_agents = list(set(state.get("completed_agents", []) + ["risk_scorer"]))
    return {"risk_score": risk_score.strip(), "completed_agents": completed_agents}
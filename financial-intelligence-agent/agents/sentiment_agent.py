
from gateway.llm_gateway import call_llm
from metrics.tracker import track_agent


def sentiment_agent(state):
    news_sentiment = state["news_summary"]
    sec_sentiment = state["sec_summary"]
    completed_agents = state.get("completed_agents", [])
    combined_input = f"News Sentiment: {news_sentiment}\n\nSEC Sentiment: {sec_sentiment}\n\nOverall Sentiment:"
    
    sentiment = track_agent("sentiment_agent", [
        {"role": "system", "content": "You are a financial analyst. Based on the news summary and SEC summary, determine the overall sentiment towards the company. Be concise and focus on key positives and negatives."},
        {"role": "user", "content": combined_input}
    ])
    completed_agents = list(set(state.get("completed_agents", []) + ["sentiment_agent"]))
    return {"sentiment": sentiment.strip(), "completed_agents": completed_agents}

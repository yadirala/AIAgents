from gateway.llm_gateway import call_llm
from agents.financialstate import FinancialState
from tavily import TavilyClient
import os

def news_fetcher(state: FinancialState) -> FinancialState:
    print("DEBUG: news_fetcher running")
    company = state["company"]
    completed = state.get("completed_agents", [])

    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    result = tavily_client.search(query=f"latest news {company}", max_results=5)
    news_data = "\n".join([r["content"] for r in result["results"]])

    news_summary = call_llm([
        {"role": "system", "content": "You are a financial analyst. Summarize the following news articles related to the company."},
        {"role": "user", "content": f"News articles: {news_data}"}
    ])
    completed = list(set(state.get("completed_agents", []) + ["news_fetcher"]))

    return {"news_summary": news_summary, "completed_agents": completed}
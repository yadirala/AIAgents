from langgraph.graph import StateGraph, START, END
from agents.financialstate import FinancialState
from agents.orchestrator import orchestrator
from agents.news_fetcher import news_fetcher
from agents.sec_agent import sec_agent
from agents.sentiment_agent import sentiment_agent
from agents.risk_scorer import risk_scorer
from agents.report_writer import report_writer

graph = StateGraph(FinancialState)

# add all nodes
graph.add_node("orchestrator", orchestrator)
graph.add_node("news_fetcher", news_fetcher)
graph.add_node("sec_agent", sec_agent)
graph.add_node("sentiment_agent", sentiment_agent)
graph.add_node("risk_scorer", risk_scorer)
graph.add_node("report_writer", report_writer)


# orchestrator runs first
graph.add_conditional_edges(START, orchestrator, ["news_fetcher", "sec_agent"])


# fan-in — both point to sentiment_agent
graph.add_edge("news_fetcher", "sentiment_agent")
graph.add_edge("sec_agent", "sentiment_agent")

# sequential after fan-in
graph.add_edge("sentiment_agent", "risk_scorer")
graph.add_edge("risk_scorer", "report_writer")
graph.add_edge("report_writer", END)

app = graph.compile()


# if __name__ == "__main__":
#     from dotenv import load_dotenv
#     load_dotenv()
    
#     print("Starting invoke...")
    
#     result = app.invoke({
#         "company": "AAPL",
#         "question": "What is the latest news about Apple?",
#         "news_summary": "",
#         "sec_summary": "",
#         "sentiment": "",
#         "risk_score": "",
#         "final_report": ""
#     })
    
#     print("Invoke complete")
#     print("Full result:", result)
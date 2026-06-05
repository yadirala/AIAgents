from langgraph.graph import StateGraph, START, END
from agents.orchestrator import orchestrator
from agents.news_fetcher import news_fetcher
from agents.sec_agent import sec_agent
from agents.sentiment_agent import sentiment_agent
from agents.risk_scorer import risk_scorer
from agents.report_writer import report_writer

from agents.financialstate import FinancialState


def router(state):
    agents_to_run = state["agents_to_run"]
    completed = set(state.get("completed_agents", []))
    
    for agent in agents_to_run:
        if agent not in completed:
            print(f"DEBUG: routing to {agent}")
            return agent
    
    print("DEBUG: routing to END")
    return END

graph = StateGraph(FinancialState)

graph.add_node("orchestrator", orchestrator)
graph.add_node("news_fetcher", news_fetcher)
graph.add_node("sec_agent", sec_agent)
graph.add_node("sentiment_agent", sentiment_agent)
graph.add_node("risk_scorer", risk_scorer)
graph.add_node("report_writer", report_writer)

graph.add_edge(START, "orchestrator")

graph.add_conditional_edges("orchestrator", router, {
    "news_fetcher": "news_fetcher",
    "sec_agent": "sec_agent",
    "sentiment_agent": "sentiment_agent",
    "risk_scorer": "risk_scorer",
    "report_writer": "report_writer",
    END: END
})

for node in ["news_fetcher", "sec_agent", "sentiment_agent", "risk_scorer", "report_writer"]:
    graph.add_conditional_edges(node, router, {
        "news_fetcher": "news_fetcher",
        "sec_agent": "sec_agent",
        "sentiment_agent": "sentiment_agent",
        "risk_scorer": "risk_scorer",
        "report_writer": "report_writer",
        END: END
    })

app = graph.compile()

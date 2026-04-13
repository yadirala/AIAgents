from typing import TypedDict, List
from openai import OpenAI
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langgraph.graph import StateGraph

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# print(os.getenv("TAVILY_API_KEY"))

class ResearchState(TypedDict):
    question: str
    search_queries: List[str]
    search_results: List[str]
    summary: str
    final_report: str

def orchestrator(state: ResearchState) -> dict:
    question = state["question"]
    messages = [{"role": "system", "content": "You are a helpful research assistant. Be concise."},
                {"role": "user", "content": f"Break the user's question {question} into exactly 3 focused search queries.Return them as a plain list, one per line, no numbers or bullets."}]
    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages)
    queries = [q.strip() for q in final_response.choices[0].message.content.strip().split("\n") if q.strip()]
    return {"search_queries": queries}




def search_agent(state: ResearchState) -> dict:
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    queries = state["search_queries"]
    final_results = []
    for query in queries:
        result = tavily.search(query=query, max_results=3)
        for r in result["results"]:
            final_results.append(r["content"])
    return {"search_results": final_results}



def analyst_agent(state: ResearchState) -> dict:
    context = "\n".join(state["search_results"])
    messages = [{"role": "system", "content": "You are a helpful research assistant. Be concise."},
                {"role": "user", "content": f"Context: {context}\n\nSummarize key findings"}]
    final_summary = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages)
    return {"summary": final_summary.choices[0].message.content}

def writer_agent(state: ResearchState) -> dict:
    
    question = state["question"]
    summary = state["summary"]
    
    messages = [{"role": "system", "content": "You are a helpful research assistant. Be concise."},
                {"role": "user", "content": f"write final report for question {question} using summary {summary}"}]
    final_result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages)
    return {"final_report": final_result.choices[0].message.content}

# Build the graph
graph = StateGraph(ResearchState)

# Add nodes
graph.add_node("orchestrator", orchestrator)
graph.add_node("search_agent", search_agent)
graph.add_node("analyst_agent", analyst_agent)
graph.add_node("writer_agent", writer_agent)

# Add edges
graph.add_edge("orchestrator", "search_agent")
graph.add_edge("search_agent", "analyst_agent")
graph.add_edge("analyst_agent", "writer_agent")

# Set entry point
graph.set_entry_point("orchestrator")

# Compile
app = graph.compile()

# final_state = app.invoke({
#     "question": "Best neighborhoods in Austin for families under $500k?",
#     "search_queries": [],
#     "search_results": [],
#     "summary": "",
#     "final_report": ""
# })

# print(final_state["final_report"])

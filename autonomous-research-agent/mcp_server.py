from mcp.server.fastmcp import FastMCP
from week2_langgraph import app

mcp = FastMCP("Research Agent")

@mcp.tool()
def research_topic(question: str) -> str:
    final_state = app.invoke({
        "question": question,      # ← use the parameter here
        "search_queries": [],
        "search_results": [],
        "summary": "",
        "final_report": ""
    })
    return final_state["final_report"]

if __name__ == "__main__":
    mcp.run()
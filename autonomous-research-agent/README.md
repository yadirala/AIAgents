# Autonomous Research Agent

A multi-agent AI system that takes a complex research question, searches the web, analyzes the results, and produces a structured report — automatically.

## What it does

You ask a question like "Best neighborhoods in Austin for families under $500k?" and the agent:
1. Breaks it into focused search queries
2. Searches the web in parallel
3. Analyzes and summarizes the findings
4. Writes a structured final report

## Architecture
User Question
↓
Orchestrator Agent — breaks question into 3 search queries
↓
Search Agent — searches web in parallel using Tavily
↓
Analyst Agent — summarizes findings
↓
Writer Agent — produces final formatted report

## Tech Stack

- **LangGraph** — multi-agent orchestration
- **OpenAI GPT-4o-mini** — LLM for all agents
- **Tavily** — real-time web search
- **ChromaDB** — vector database for RAG
- **FastAPI** — REST API
- **Docker** — containerization
- **Railway** — cloud deployment
- **MCP** — Claude Desktop integration
- **LangSmith** — observability and tracing

## Features

- Multi-agent pipeline with LangGraph
- Parallel web search — 3x faster than sequential
- RAG-style analysis with ChromaDB
- MCP server compatible with Claude Desktop and Cursor
- REST API with auto-generated Swagger docs
- Fully containerized with Docker
- Deployed on Railway with live public URL

## How to Run Locally

1. Clone the repo
```bash
git clone https://github.com/yadirala/AIAgents.git
cd AIAgents/autonomous-research-agent
```

2. Create `.env` file with your API keys
OPENAI_API_KEY=your-key
TAVILY_API_KEY=your-key
LANGSMITH_API_KEY=your-key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=Research AI Agent

3. Set up virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Run the server
```bash
uvicorn api:app --reload
```

5. Open Swagger UI at `http://127.0.0.1:8000/docs`

## API
POST /research
Content-Type: application/json
{
"question": "your research question here"
}

## MCP Server

Connect to Claude Desktop by adding to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "research-agent": {
      "command": "/path/to/.venv/bin/python3",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

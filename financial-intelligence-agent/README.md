# Financial Intelligence Agent

A production-grade multi-agent AI system that analyzes company investment risk using real-time news, SEC filings, and AI-powered analysis.

## What it does

You provide a company ticker and question like "What is Apple's investment risk for 2025?" and the agent:

1. Dynamically decides which agents to run based on your question
2. Fetches real-time news via Tavily
3. Analyzes SEC 10-K filings using vectorless RAG
4. Assesses market sentiment
5. Scores investment risk 1-10
6. Generates a structured research report
7. Evaluates report quality using LLM-as-a-judge

## Architecture
User Question + Ticker
↓
PII Guardrail
↓
Orchestrator (deep agent planner)
↓
News Fetcher → SEC Agent → Sentiment → Risk Scorer → Report Writer
↓
Human Approval (if risk ≥ 8)
↓
LLM Evaluator
↓
Final Report + Quality Scores

## Tech Stack

- **LangGraph** — multi-agent orchestration with dynamic routing
- **LiteLLM** — LLM gateway with fallback (GPT-4o-mini → Gemini → Groq)
- **OpenAI GPT-4o-mini** — primary LLM
- **Tavily** — real-time web search
- **SEC EDGAR** — 10-K filing retrieval
- **Vectorless RAG** — hierarchical JSON index on SEC filings
- **FastAPI** — REST API
- **Docker** — containerization

## Features

- Deep agent architecture — orchestrator dynamically plans which agents to run
- Vectorless RAG — no vector DB needed for SEC filing analysis
- LLM gateway with automatic fallback across providers
- PII detection and redaction on all inputs
- Human-in-the-loop approval for high risk reports
- LLM-as-a-judge evaluation scoring every report

## How to Run Locally

1. Clone the repo
```bash
git clone https://github.com/yadirala/AIAgents.git
cd AIAgents/financial-intelligence-agent
```

2. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Create `.env` file
OPENAI_API_KEY=your-key
TAVILY_API_KEY=your-key
LANGSMITH_API_KEY=your-key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=Financial Intelligence Agent

4. Run the server
```bash
uvicorn api:app --reload
```

5. Open Swagger UI at `http://127.0.0.1:8000/docs`

## API
POST /analyze
Content-Type: application/json
{
"company": "AAPL",
"question": "What is Apple's investment risk for 2025?"
}

## Response

```json
{
  "final_report": "# Investment Research Report...",
  "evaluation": {
    "accuracy": 8,
    "relevance": 9,
    "groundedness": 8,
    "conciseness": 7,
    "overall": 8,
    "feedback": "..."
  }
}
```

## Docker

```bash
docker build -t financial-intelligence-agent .
docker run -p 8000:8000 --env-file .env financial-intelligence-agent
```

## Phase 2 Roadmap

- LangGraph Send API for cleaner dynamic routing
- Fan-out/Fan-in parallel execution for News + SEC agents
- LangGraph checkpointing for resumable pipelines
- Redis state management for distributed deployments
- Full 10-K coverage with section-based splitting
- Support for 10-Q and 8-K filings
- LangSmith observability integration
- Metrics tracking — latency, cost, success rate per agent

from rag.sec_rag import get_cik, fetch_sec_filing, build_index
from gateway.llm_gateway import call_llm
from agents.financialstate import FinancialState
import json

def sec_agent(state: FinancialState) -> dict:
    # 1. get company and question from state
    # 2. get CIK
    # 3. fetch filing
    # 4. build/load index
    # 5. send index + question to LLM to extract relevant info
    # 6. return {"sec_summary": answer}
    company = state["company"]
    question = state["question"]
    completed = state.get("completed_agents", [])   
    cik = get_cik(company)
    filing_content = fetch_sec_filing(cik)
    index = build_index(filing_content, company)
    answer = call_llm([
        {"role": "system", "content": "You are a financial analyst. Use the following indexed information from the company's 10-K filing to answer the question. Be concise and focus on relevant sections."},
        {"role": "user", "content": f"Index: {json.dumps(index)}\n\nQuestion: {question}"}
    ])
    completed = list(set(state.get("completed_agents", []) + ["sec_agent"]))
    return {"sec_summary": answer, "completed_agents": completed}
from rag.sec_rag import get_cik, fetch_sec_filing, build_index
from gateway.llm_gateway import call_llm
from agents.financialstate import FinancialState
import json

def sec_agent(state):
    company = state["company"]
    question = state["question"]
    cik = get_cik(company)
    filing_content = fetch_sec_filing(cik)
    index = build_index(filing_content, company)
    
    # build context using summaries for routing + content for depth
    context = ""
    for section_name, data in index.items():
        context += f"\n\n{section_name.upper()}:\n{data['summary']}\n\nDetailed content:\n{data['content'][:2000]}"
    
    answer = call_llm([
        {"role": "system", "content": "You are a financial analyst. Use the SEC filing sections to answer the question accurately."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ])
    
    return {"sec_summary": answer}


from gateway.llm_gateway import call_llm


def report_writer(state):
    company = state["company"]
    question = state["question"]
    news_summary = state["news_summary"]
    sec_summary = state["sec_summary"]
    sentiment = state["sentiment"]
    risk_score = state["risk_score"]
    completed_agents = state.get("completed_agents", [])
    report_input = f"Company: {company}\n\nQuestion: {question}\n\nNews Summary: {news_summary}\n\nSEC Summary: {sec_summary}\n\nSentiment: {sentiment}\n\nRisk Score: {risk_score}\n\nWrite a structured investment research report based on the above information. Include sections like Executive Summary, News Analysis, SEC Filing Analysis, Sentiment Assessment, Risk Score, and Recommendation."
    
    final_report = call_llm([
        {"role": "system", "content": "You are a financial analyst. Write a comprehensive investment research report based on the provided information. Be concise and focus on key insights."},
        {"role": "user", "content": report_input}
    ])
    completed = list(set(state.get("completed_agents", []) + ["report_writer"]))

    return {"final_report": final_report.strip(), "completed_agents": completed}
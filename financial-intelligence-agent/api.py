import uuid
from dotenv import load_dotenv
load_dotenv()

from graph import app as research_app
from fastapi import FastAPI
from pydantic import BaseModel
from guardrails.pii_guard import redact_pii
from guardrails.human_loop import requires_human_approval, get_human_approval
from evaluation.evaluator import evaluate_report

app = FastAPI()

class AnalyzeRequest(BaseModel):
    company: str
    question: str

class AnalyzeResponse(BaseModel):
    final_report: str
    evaluation: dict

@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    clean_question = redact_pii(request.question)
    
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    result = research_app.invoke({
        "company": request.company,
        "question": clean_question,
        "news_summary": "",
        "sec_summary": "",
        "sentiment": "",
        "risk_score": "",
        "final_report": ""
    }, config=config)
    
    risk_score = result["risk_score"]
    final_report = result["final_report"]
    
    if requires_human_approval(risk_score):
        approved = get_human_approval(final_report)
        if not approved:
            final_report = "Report rejected by human reviewer."
    
    evaluation = evaluate_report(request.question, final_report)
    return AnalyzeResponse(final_report=final_report, evaluation=evaluation)
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()

from week2_langgraph import app as reserach_app

app = FastAPI()
class ResearchRequest(BaseModel):
    question: str

class ResearchResponse(BaseModel):
    report: str
    
@app.post("/research")
def research(request: ResearchRequest) -> ResearchResponse:
    final_state = reserach_app.invoke({
    "question": request.question,
    "search_queries": [],
    "search_results": [],
    "summary": "",
    "final_report": ""})
    return ResearchResponse(report=final_state["final_report"])

from typing import List, TypedDict, Annotated

import operator

class FinancialState(TypedDict):
    company: str
    question: str
    news_summary: str
    sec_summary: str
    sentiment: str
    risk_score: str
    final_report: str
    agents_to_run: List[str]
    completed_agents: List[str]
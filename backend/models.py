from pydantic import BaseModel
from typing import List, Optional

class GapItem(BaseModel):
    area: str
    description: str
    severity: str

class ActionItem(BaseModel):
    action: str
    priority: str
    timeline: str

class AnalyzeRequest(BaseModel):
    standard: str

class ScoreRequest(BaseModel):
    session_id: int
    question_index: int
    question: str
    answer: str
    expected_topics: list
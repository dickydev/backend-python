from pydantic import BaseModel
from datetime import datetime

class FeedbackForm(BaseModel):
    score: int
    comment: str
    created_at: datetime

    class Config:
        orm_mode = True
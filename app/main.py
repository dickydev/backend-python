from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, schemas
from fastapi import Depends
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/feedback/")
def create_feedback(feedback: schemas.FeedbackForm, db: Session = Depends(get_db)):
    db_feedback = models.Feedback(score=feedback.score, comment=feedback.comment, created_at=feedback.created_at)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.get("/feedback/{feedback_id}")
def read_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@app.get("/feedback/")
def read_all_feedbacks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    feedbacks = db.query(models.Feedback).offset(skip).limit(limit).all()
    return feedbacks

@app.delete("/feedback/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    db.delete(db_feedback)
    db.commit()
    return {"message": "Feedback deleted successfully"}

@app.put("/feedback/{feedback_id}")
def update_feedback(feedback_id: int, feedback: schemas.FeedbackForm, db: Session = Depends(get_db)):
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    db_feedback.score = feedback.score
    db_feedback.comment = feedback.comment
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.get("/")
def read_root():
    return {"message": "Welcome to the Feedback API with FastAPI and SQLAlchemy"}
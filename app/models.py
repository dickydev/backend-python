from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)
    comment = Column(String)
    created_at = Column(DateTime, nullable=False)
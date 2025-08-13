# db.py
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in .env")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class MatchResult(Base):
    __tablename__ = "match_results"
    id = Column(Integer, primary_key=True, index=True)
    resume_path = Column(String(512))
    job_path = Column(String(512))
    match_score = Column(Float)
    summary = Column(Text)
    suggestions = Column(Text)   # JSON serialized str
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_result(resume_path: str, job_path: str, report: dict):
    session = SessionLocal()
    try:
        rec = MatchResult(
            resume_path=resume_path,
            job_path=job_path,
            match_score=float(report.get("match_score", 0.0)),
            summary=report.get("summary", ""),
            suggestions=json.dumps({
                "strengths": report.get("strengths", []),
                "gaps": report.get("gaps", []),
                "improvements": report.get("improvements", [])
            })
        )
        session.add(rec)
        session.commit()
    finally:
        session.close()

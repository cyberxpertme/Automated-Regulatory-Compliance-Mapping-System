# upload_history.py
# Phase 14: Store uploaded document analysis results permanently

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class UploadHistory(Base):
    __tablename__ = "upload_history"

    id = Column(Integer, primary_key=True, index=True)
    uploaded_by = Column(String, nullable=True)  # user email
    total_files = Column(Integer, default=0)
    total_clauses_mapped = Column(Integer, default=0)
    average_confidence = Column(Float, default=0.0)
    high_confidence_count = Column(Integer, default=0)
    low_confidence_count = Column(Integer, default=0)
    file_breakdown = Column(Text, nullable=True)   # JSON string
    function_distribution = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UploadClause(Base):
    __tablename__ = "upload_clauses"

    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("upload_history.id"))
    source_file = Column(String, nullable=False)
    source_text = Column(Text, nullable=False)
    matched_nist_control = Column(String, nullable=False)
    matched_nist_title = Column(String, nullable=True)
    nist_function = Column(String, nullable=True)
    confidence_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

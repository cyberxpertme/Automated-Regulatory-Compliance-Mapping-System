# compliance.py
# Phase 2: Control mapping model

from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class ControlMapping(Base):
    __tablename__ = "control_mappings"

    id = Column(Integer, primary_key=True, index=True)

    # Source: ISO 27001
    source_framework = Column(String, nullable=False)
    source_control_id = Column(String, nullable=False)
    source_control_title = Column(String, nullable=False)
    source_control_text = Column(Text, nullable=True)

    # Target: NIST CSF
    target_framework = Column(String, nullable=False)
    target_control_id = Column(String, nullable=False)
    target_control_title = Column(String, nullable=False)

    # Mapping quality
    confidence_score = Column(Float, default=0.0)
    gap_description = Column(Text, nullable=True)
    organization = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Integer, JSON
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class HistoricalIncident(Base):
    __tablename__ = 'historical_incidents'

    id = Column(String(64), primary_key=True)
    incident_type = Column(String(100), nullable=False)
    raw_logs = Column(Text, nullable=False)
    remediation_playbook = Column(Text, nullable=False)
    embedding = Column(Vector(1536), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ActiveRemediation(Base):
    __tablename__ = 'active_remediations'

    remediation_id = Column(String(64), primary_key=True)
    cluster_id = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="INITIATED")
    current_step = Column(Integer, nullable=False, default=1)
    matched_incident_id = Column(String(64), nullable=True)
    execution_context = Column(JSON, nullable=False, default={})
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

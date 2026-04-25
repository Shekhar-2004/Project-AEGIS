from sqlalchemy import Column, Integer, Float, String, DateTime
from backend.db.base import Base
from datetime import datetime, timezone
import uuid


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    video_id = Column(String, index=True)
    video_source = Column(String)

    object_1 = Column(String)
    object_2 = Column(String)

    distance_m = Column(Float)
    ttc_seconds = Column(Float)
    relative_velocity = Column(Float)

    nmrs_score = Column(Float)
    risk_level = Column(String)

    frame_number = Column(Integer)

    ai_summary = Column(String, nullable=True)
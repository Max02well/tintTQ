from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, func
from app.db.base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=True)
    
    report_type = Column(String)                         # tint_recommendation, damage_analysis
    content = Column(JSON, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
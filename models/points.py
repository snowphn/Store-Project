from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.db_init import Base

class PointsTransaction(Base):
    __tablename__ = "points_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)  # 正数表示增加，负数表示减少
    type = Column(String(20), nullable=False)  # recharge, purchase, refund
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联关系
    user = relationship("User", back_populates="points_transactions")
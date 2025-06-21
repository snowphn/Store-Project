from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.db_init import Base

CATEGORY_CHOICES = [
    ("皮肤", "皮肤"),
    ("枪模", "枪模"),
    ("特效", "特效"),
    ("积分", "积分"),
    ("特权", "特权")
]

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)  # 积分价格
    stock = Column(Integer, default=0)
    image_url = Column(String(255))
    category = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    cart_items = relationship("CartItem", back_populates="product")
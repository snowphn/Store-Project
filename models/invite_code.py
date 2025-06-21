from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from database.db_init import Base
import enum

class PrivilegeType(enum.Enum):
    """特权类型枚举"""
    NORMAL = "normal"      # 普通用户
    VIP = "vip"           # VIP用户
    ADMIN = "admin"       # 管理员

class InviteCode(Base):
    __tablename__ = "invite_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    privilege_type = Column(Enum(PrivilegeType), default=PrivilegeType.NORMAL, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    used_at = Column(DateTime(timezone=True), nullable=True)
    used_by_user_id = Column(Integer, nullable=True)  # 记录使用该邀请码的用户ID

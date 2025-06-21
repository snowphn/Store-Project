from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.db_init import Base
from models.invite_code import PrivilegeType
from utils.password import hash_password, verify_password
from utils.image_utils import compress_image, image_to_base64, base64_to_image, save_avatar, load_avatar
import hashlib
from models.order import Order
from models.cart import CartItem
from models.points import PointsTransaction

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    password_salt = Column(String(128), nullable=False)
    points = Column(Integer, default=0)
    user_type = Column(Enum(PrivilegeType), default=PrivilegeType.NORMAL, nullable=False)  # 用户类型
    display_name = Column(String(100), nullable=True)  # 显示名称
    is_admin = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)  # 是否被封禁
    avatar = Column(String(100), default="default_avatar.jpg")  # 头像文件名
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 
    permissions = Column(String, default="[]")  # 存储管理员权限的JSON字符串
    invite_code_used = Column(String(20), nullable=True)  # 使用的邀请码

    # 关联关系
    steam_binding = relationship("SteamBinding", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")
    points_transactions = relationship("PointsTransaction", back_populates="user")

    def set_password(self, password):
        """设置密码"""
        self.password_hash, self.password_salt = hash_password(password)
        
    def check_password(self, password):
        """验证密码"""
        if not self.password_salt:
            # 兼容老用户（无盐值，直接hash）
            return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
        return verify_password(password, self.password_hash, self.password_salt)
        
    def set_avatar(self, avatar_data):
        """设置用户头像"""
        try:
            # 压缩图片
            compressed_data = compress_image(avatar_data)
            
            # 保存头像文件
            filename = save_avatar(compressed_data, self.id)
            if filename:
                self.avatar = filename
                return True
            return False
        except Exception as e:
            print(f"设置头像失败: {str(e)}")
            return False
    
    def get_avatar_data(self):
        """获取用户头像数据"""
        try:
            return load_avatar(self.avatar)
        except Exception as e:
            print(f"加载头像失败: {str(e)}")
            return None
    
    def generate_display_name(self):
        """根据用户类型自动生成显示名称"""
        if self.user_type == PrivilegeType.ADMIN:
            self.display_name = f"管理员 {self.username}"
        elif self.user_type == PrivilegeType.VIP:
            self.display_name = f"VIP {self.username}"
        else:
            self.display_name = f"用户 {self.username}"
    
    def get_type_display(self):
        """获取用户类型的显示文本"""
        type_map = {
            PrivilegeType.ADMIN: "管理员",
            PrivilegeType.VIP: "VIP用户",
            PrivilegeType.NORMAL: "普通用户"
        }
        return type_map.get(self.user_type, "普通用户")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', user_type='{self.user_type}')>"
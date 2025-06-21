from database.db_init import SessionLocal
from models.user import User
from werkzeug.security import generate_password_hash
import json

def create_admin_user(username, password, permissions):
    """创建管理员用户"""
    db = SessionLocal()
    try:
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            return False, "用户名已存在"
            
        # 创建新管理员
        admin = User(
            username=username,
            email=f"{username}@example.com",  # 临时邮箱
            is_admin=True,
            points=0,
            permissions=json.dumps(permissions)  # 将权限字典转换为JSON字符串
        )
        admin.set_password(password)
        db.add(admin)
        db.commit()
        return True, "管理员账号创建成功"
    except Exception as e:
        db.rollback()
        return False, f"创建管理员账号失败: {str(e)}"
    finally:
        db.close()

def get_user_by_username(username):
    """根据用户名获取用户"""
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()

def get_user_by_id(user_id):
    """根据ID获取用户"""
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()

def update_user_points(user_id, points):
    """更新用户积分"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.points = points
            db.commit()
            return True, "积分更新成功"
        return False, "用户不存在"
    except Exception as e:
        db.rollback()
        return False, f"更新积分失败: {str(e)}"
    finally:
        db.close()

def ban_user(user_id):
    """封禁用户"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_banned = not user.is_banned
            db.commit()
            return True, "用户状态已更新"
        return False, "用户不存在"
    except Exception as e:
        db.rollback()
        return False, f"更新用户状态失败: {str(e)}"
    finally:
        db.close() 
from sqlalchemy.orm import Session
from database.db_init import SessionLocal
from models.user import User
from models.product import Product
from models.order import Order
from models.points import PointsTransaction
from models.steam_binding import SteamBinding
from models.cart import CartItem
from utils.password import hash_password, verify_password
from datetime import datetime
from typing import List, Optional
import random
import string
from sqlalchemy import func
from models.invite_code import InviteCode

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_test_data():
    """初始化测试数据"""
    db = SessionLocal()
    try:
        # 检查是否已有数据
        if db.query(Product).first():
            return
        
        db.commit()
    finally:
        db.close()

def get_products() -> list:
    """获取所有商品"""
    db = SessionLocal()
    try:
        return db.query(Product).all()
    finally:
        db.close()

def create_user(username: str, email: str, password: str, invite_code: str = None) -> tuple[bool, str]:
    """创建新用户"""
    from models.invite_code import PrivilegeType
    db = SessionLocal()
    try:
        # 检查用户名和邮箱是否已存在
        if db.query(User).filter(User.username == username).first():
            return False, "用户名已存在"
        if db.query(User).filter(User.email == email).first():
            return False, "邮箱已被注册"
        
        # 确定用户类型
        user_type = PrivilegeType.NORMAL
        invite_code_used = None
        
        if invite_code:
            # 验证并使用邀请码
            privilege_type = use_invite_code(invite_code, None)  # 先传None，后面更新
            if privilege_type:
                # 禁止通过邀请码注册管理员账户
                if privilege_type == PrivilegeType.ADMIN:
                    return False, "管理员账户只能由超级管理员后台创建"
                user_type = privilege_type
                invite_code_used = invite_code
            else:
                return False, "邀请码无效或已使用"
        
        # 创建新用户
        password_hash, password_salt = hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            password_salt=password_salt,
            user_type=user_type,
            invite_code_used=invite_code_used
        )
        
        # 设置管理员权限
        if user_type == PrivilegeType.ADMIN:
            user.is_admin = True
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # 更新邀请码的使用者ID
        if invite_code_used:
            db.query(InviteCode).filter(InviteCode.code == invite_code_used).update(
                {"used_by_user_id": user.id}
            )
            db.commit()
        
        return True, "用户创建成功"
    except Exception as e:
        db.rollback()
        return False, f"创建用户失败: {str(e)}"
    finally:
        db.close()

def verify_user(username: str, password: str) -> User:
    """验证用户登录"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and verify_password(password, user.password_hash):
            return user
        return None
    finally:
        db.close()

def get_user_by_id(user_id: int) -> User:
    """通过ID获取用户"""
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()

def update_user_points(user_id: int, points: float) -> User:
    """更新用户积分"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.points += points
            db.commit()
            db.refresh(user)
        return user
    finally:
        db.close()

def create_points_transaction(user_id: int, amount: float, type: str, description: str) -> PointsTransaction:
    """创建积分交易记录"""
    db = SessionLocal()
    try:
        transaction = PointsTransaction(
            user_id=user_id,
            amount=amount,
            type=type,
            description=description
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    finally:
        db.close()

def get_user_transactions(user_id: int) -> list:
    """获取用户积分交易记录"""
    db = SessionLocal()
    try:
        return db.query(PointsTransaction).filter(
            PointsTransaction.user_id == user_id
        ).order_by(PointsTransaction.created_at.desc()).all()
    finally:
        db.close()

def bind_steam_account(user_id: int, steam_id: str, steam_name: str) -> SteamBinding:
    """绑定Steam账号"""
    db = SessionLocal()
    try:
        # 检查是否已绑定
        existing = db.query(SteamBinding).filter(
            SteamBinding.steam_id == steam_id
        ).first()
        if existing:
            raise ValueError("该Steam账号已被绑定")
        
        binding = SteamBinding(
            user_id=user_id,
            steam_id=steam_id,
            steam_name=steam_name
        )
        db.add(binding)
        db.commit()
        db.refresh(binding)
        return binding
    finally:
        db.close()

def get_steam_binding(user_id: int) -> SteamBinding:
    """获取用户的Steam绑定信息"""
    db = SessionLocal()
    try:
        return db.query(SteamBinding).filter(
            SteamBinding.user_id == user_id
        ).first()
    finally:
        db.close()

def get_cart_items(user_id: int) -> list:
    """获取用户的购物车商品"""
    db = SessionLocal()
    try:
        # 使用joinedload预加载product关联数据，避免DetachedInstanceError
        from sqlalchemy.orm import joinedload
        cart_items = db.query(CartItem).options(joinedload(CartItem.product)).filter(CartItem.user_id == user_id).all()
        # 确保所有关联数据都已加载
        for item in cart_items:
            _ = item.product.name  # 触发加载
            _ = item.product.price
        return cart_items
    finally:
        db.close()

def add_to_cart(user_id: int, product_id: int, quantity: int = 1) -> tuple[bool, str]:
    """添加商品到购物车"""
    db = SessionLocal()
    try:
        # 检查商品是否已在购物车中
        cart_item = db.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
            message = "商品数量已更新"
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            db.add(cart_item)
            message = "商品已添加到购物车"
        
        db.commit()
        db.refresh(cart_item)
        return True, message
    except Exception as e:
        db.rollback()
        return False, f"添加失败: {str(e)}"
    finally:
        db.close()

def remove_from_cart(cart_item_id: int) -> bool:
    """从购物车中移除商品"""
    db = SessionLocal()
    try:
        cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
        if cart_item:
            db.delete(cart_item)
            db.commit()
            return True
        return False
    finally:
        db.close()

def update_cart_item(cart_item_id: int, quantity: int) -> tuple[bool, str]:
    """更新购物车商品数量"""
    db = SessionLocal()
    try:
        cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
        if not cart_item:
            return False, "购物车商品不存在"
        
        if quantity <= 0:
            return False, "数量必须大于0"
        
        cart_item.quantity = quantity
        db.commit()
        return True, "更新成功"
    except Exception as e:
        db.rollback()
        return False, f"更新失败: {str(e)}"
    finally:
        db.close()

def create_order(user_id: int) -> Order:
    """创建订单"""
    db = SessionLocal()
    try:
        # 获取购物车商品
        cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
        if not cart_items:
            raise ValueError("购物车为空")
        
        # 计算总积分并收集商品信息
        total_points = 0
        order_items = []
        for item in cart_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product or product.stock < item.quantity:
                raise ValueError(f"商品 {product.name if product else '未知'} 库存不足")
            
            total_points += product.price * item.quantity
            order_items.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "subtotal": product.price * item.quantity
            })
        
        # 检查用户积分是否足够
        user = db.query(User).filter(User.id == user_id).first()
        if user.points < total_points:
            raise ValueError("积分不足")
        
        # 创建订单
        order = Order(
            user_id=user_id,
            total_points=total_points,
            status="pending",
            items=order_items
        )
        db.add(order)
        
        # 扣除用户积分
        user.points -= total_points
        
        # 更新商品库存
        for item in cart_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            product.stock -= item.quantity
        
        # 清空购物车
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        
        db.commit()
        db.refresh(order)
        return order
    finally:
        db.close()

def get_all_users() -> list:
    """获取所有用户"""
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()

def get_all_products() -> list:
    """获取所有商品"""
    db = SessionLocal()
    try:
        return db.query(Product).all()
    finally:
        db.close()

def get_all_orders() -> list:
    """获取所有订单"""
    db = SessionLocal()
    try:
        return db.query(Order).all()
    finally:
        db.close()

def create_product(name: str, description: str, price: float, stock: int, category: str) -> tuple[bool, str]:
    """创建新商品"""
    db = SessionLocal()
    try:
        # 检查商品名是否已存在
        if db.query(Product).filter(Product.name == name).first():
            return False, "商品名已存在"
        
        # 创建新商品
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        return True, "商品创建成功"
    except Exception as e:
        db.rollback()
        return False, f"创建商品失败: {str(e)}"
    finally:
        db.close()

def update_product(product_id: int, **kwargs) -> tuple[bool, str]:
    """更新商品信息"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False, "商品不存在"
        
        # 如果更新名称，检查新名称是否与其他商品重复
        if 'name' in kwargs and kwargs['name'] != product.name:
            if db.query(Product).filter(Product.name == kwargs['name']).first():
                return False, "商品名已存在"
        
        # 更新商品信息
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        db.commit()
        db.refresh(product)
        return True, "商品更新成功"
    except Exception as e:
        db.rollback()
        return False, f"更新商品失败: {str(e)}"
    finally:
        db.close()

def delete_product(product_id: int) -> tuple[bool, str]:
    """删除商品"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False, "商品不存在"
        
        db.delete(product)
        db.commit()
        return True, "商品删除成功"
    except Exception as e:
        db.rollback()
        return False, f"删除商品失败: {str(e)}"
    finally:
        db.close()

def get_user_by_username(username: str) -> User:
    """根据用户名获取用户信息"""
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()

def get_user_points_transactions(user_id: int) -> List[PointsTransaction]:
    """
    获取用户的积分交易记录
    
    Args:
        user_id: 用户ID
        
    Returns:
        List[PointsTransaction]: 积分交易记录列表
    """
    session = SessionLocal()
    try:
        transactions = session.query(PointsTransaction)\
            .filter_by(user_id=user_id)\
            .order_by(PointsTransaction.created_at.desc())\
            .all()
        return transactions
    finally:
        session.close()

def unbind_steam_account(user_id: int) -> bool:
    """解绑Steam账号"""
    db = SessionLocal()
    try:
        binding = db.query(SteamBinding).filter(
            SteamBinding.user_id == user_id
        ).first()
        
        if binding:
            db.delete(binding)
            db.commit()
            return True
        return False
    finally:
        db.close()

def update_user_avatar(user_id: int, avatar_path: str) -> bool:
    """
    更新用户头像
    
    Args:
        user_id: 用户ID
        avatar_path: 头像文件路径
        
    Returns:
        bool: 更新是否成功
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
            
        user.avatar = avatar_path
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"更新用户头像失败: {str(e)}")
        return False
    finally:
        db.close()

def delete_all_users():
    """
    删除所有用户及其相关数据（Steam绑定、积分记录、购物车、订单等）。
    """
    db = SessionLocal()
    try:
        db.query(SteamBinding).delete()
        db.query(PointsTransaction).delete()
        db.query(CartItem).delete()
        db.query(Order).delete()
        db.query(User).delete()
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"删除所有用户失败: {str(e)}")
        return False
    finally:
        db.close()

def delete_demo_data():
    """
    删除所有商品、购物车、订单、积分、Steam绑定等演示数据。
    """
    db = SessionLocal()
    try:
        db.query(CartItem).delete()
        db.query(Order).delete()
        db.query(Product).delete()
        db.query(PointsTransaction).delete()
        db.query(SteamBinding).delete()
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"删除演示数据失败: {str(e)}")
        return False
    finally:
        db.close()

def reset_all_data():
    """重置所有数据"""
    try:
        from database.db_init import reset_database
        return reset_database()
    except Exception as e:
        print(f"重置数据失败: {str(e)}")
        return False

def update_user_info(user_id: int, username: str = None, email: str = None, password: str = None) -> bool:
    """
    更新用户信息
    
    Args:
        user_id: 用户ID
        username: 新用户名（可选）
        email: 新邮箱（可选）
        password: 新密码（可选）
        
    Returns:
        bool: 更新是否成功
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
            
        if username:
            # 检查用户名是否已存在
            existing = db.query(User).filter(User.username == username, User.id != user_id).first()
            if existing:
                raise ValueError("用户名已存在")
            user.username = username
            
        if email:
            # 检查邮箱是否已被使用
            existing = db.query(User).filter(User.email == email, User.id != user_id).first()
            if existing:
                raise ValueError("邮箱已被使用")
            user.email = email
            
        if password:
            user.set_password(password)
            
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"更新用户信息失败: {str(e)}")
        return False
    finally:
        db.close()

def generate_invite_code(length=8):
    """生成随机邀请码"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def create_invite_code(privilege_type=None):
    """创建新的邀请码"""
    from models.invite_code import PrivilegeType
    db = SessionLocal()
    try:
        code = generate_invite_code()
        if privilege_type is None:
            privilege_type = PrivilegeType.NORMAL
        invite_code = InviteCode(code=code, privilege_type=privilege_type)
        db.add(invite_code)
        db.commit()
        db.refresh(invite_code)
        return invite_code
    finally:
        db.close()

def get_invite_codes():
    """获取所有邀请码"""
    db = SessionLocal()
    try:
        return db.query(InviteCode).all()
    finally:
        db.close()

def use_invite_code(code, user_id):
    """使用邀请码"""
    db = SessionLocal()
    try:
        invite_code = db.query(InviteCode).filter(InviteCode.code == code, InviteCode.is_used == False).first()
        if invite_code:
            invite_code.is_used = True
            invite_code.used_at = func.now()
            invite_code.used_by_user_id = user_id
            db.commit()
            return invite_code.privilege_type
        return None
    finally:
        db.close()

def verify_invite_code(code):
    from models.invite_code import InviteCode
    db = SessionLocal()
    try:
        invite = db.query(InviteCode).filter(InviteCode.code == code, InviteCode.is_used == False).first()
        return invite is not None
    finally:
        db.close()

def delete_invite_code(invite_id: int) -> bool:
    """根据ID删除邀请码"""
    db = SessionLocal()
    try:
        code = db.query(InviteCode).filter(InviteCode.id == invite_id).first()
        if code:
            db.delete(code)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"删除邀请码失败: {str(e)}")
        return False
    finally:
        db.close()

# 在文件末尾添加以下函数

def create_admin_user_with_permissions(username, email, password, permissions):
    """创建具有特定权限的管理员用户"""
    session = SessionLocal()
    try:
        # 检查用户名是否已存在
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            return False, "用户名已存在"
        
        # 检查邮箱是否已存在
        existing_email = session.query(User).filter_by(email=email).first()
        if existing_email:
            return False, "邮箱已被使用"
        
        # 创建新管理员
        from utils.password import hash_password
        password_hash, salt = hash_password(password)
        
        new_admin = User(
            username=username,
            email=email,
            password_hash=password_hash,
            password_salt=salt,
            is_admin=True,
            permissions=json.dumps(permissions)
        )
        
        session.add(new_admin)
        session.commit()
        return True, f"管理员 {username} 创建成功"
        
    except Exception as e:
        session.rollback()
        return False, f"创建管理员失败: {str(e)}"
    finally:
        session.close()

def validate_email_existence(email):
    """验证邮箱格式和存在性"""
    import re
    import dns.resolver
    
    # 基本邮箱格式验证
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False
    
    try:
        # 提取域名
        domain = email.split('@')[1]
        
        # 检查MX记录
        mx_records = dns.resolver.resolve(domain, 'MX')
        return len(mx_records) > 0
    except:
        # 如果DNS查询失败，只进行格式验证
        return True
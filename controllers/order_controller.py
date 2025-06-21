from database.db_init import SessionLocal
from models.order import Order
from models.product import Product
from models.user import User
from datetime import datetime

def create_order(user_id, items):
    """创建新订单"""
    db = SessionLocal()
    try:
        # 检查用户是否存在
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "用户不存在"
            
        # 计算总积分
        total_points = 0
        order_items = []
        
        for item in items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                return False, f"商品 {item.product_id} 不存在"
            if product.stock < item.quantity:
                return False, f"商品 {product.name} 库存不足"
                
            total_points += product.price * item.quantity
            order_items.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity
            })
            
        # 检查用户积分是否足够
        if user.points < total_points:
            return False, "积分不足"
            
        # 创建订单
        order = Order(
            user_id=user_id,
            total_points=total_points,
            status="待发货",
            items=order_items
        )
        db.add(order)
        
        # 更新用户积分
        user.points -= total_points
        
        # 更新商品库存
        for item in items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            product.stock -= item.quantity
            
        # 清空购物车
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        
        db.commit()
        return True, "订单创建成功"
    except Exception as e:
        db.rollback()
        return False, f"创建订单失败: {str(e)}"
    finally:
        db.close()

def get_order_by_id(order_id):
    """根据ID获取订单"""
    db = SessionLocal()
    try:
        return db.query(Order).filter(Order.id == order_id).first()
    finally:
        db.close()

def get_user_orders(user_id):
    """获取用户的所有订单"""
    db = SessionLocal()
    try:
        return db.query(Order).filter(Order.user_id == user_id).all()
    finally:
        db.close()

def get_all_orders():
    """获取所有订单"""
    db = SessionLocal()
    try:
        return db.query(Order).all()
    finally:
        db.close()

def update_order_status(order_id, status):
    """更新订单状态"""
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = status
            db.commit()
            return True, "订单状态更新成功"
        return False, "订单不存在"
    except Exception as e:
        db.rollback()
        return False, f"更新订单状态失败: {str(e)}"
    finally:
        db.close() 
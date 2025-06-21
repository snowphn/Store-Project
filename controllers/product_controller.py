from database.db_init import SessionLocal
from models.product import Product

def create_product(name, description, price, stock, category):
    """创建新商品"""
    db = SessionLocal()
    try:
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category
        )
        db.add(product)
        db.commit()
        return True, "商品创建成功"
    except Exception as e:
        db.rollback()
        return False, f"创建商品失败: {str(e)}"
    finally:
        db.close()

def update_product(product_id, name, description, price, stock, category):
    """更新商品信息"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.name = name
            product.description = description
            product.price = price
            product.stock = stock
            product.category = category
            db.commit()
            return True, "商品更新成功"
        return False, "商品不存在"
    except Exception as e:
        db.rollback()
        return False, f"更新商品失败: {str(e)}"
    finally:
        db.close()

def delete_product(product_id):
    """删除商品"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return True, "商品删除成功"
        return False, "商品不存在"
    except Exception as e:
        db.rollback()
        return False, f"删除商品失败: {str(e)}"
    finally:
        db.close()

def get_product_by_id(product_id):
    """根据ID获取商品"""
    db = SessionLocal()
    try:
        return db.query(Product).filter(Product.id == product_id).first()
    finally:
        db.close()

def get_all_products():
    """获取所有商品"""
    db = SessionLocal()
    try:
        return db.query(Product).all()
    finally:
        db.close()

def update_product_stock(product_id, quantity):
    """更新商品库存"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            if product.stock >= quantity:
                product.stock -= quantity
                db.commit()
                return True, "库存更新成功"
            return False, "库存不足"
        return False, "商品不存在"
    except Exception as e:
        db.rollback()
        return False, f"更新库存失败: {str(e)}"
    finally:
        db.close() 
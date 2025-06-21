import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.database import DATABASE_URL
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # 创建数据库引擎
    engine = create_engine(DATABASE_URL, echo=True)
    logger.info(f"数据库引擎创建成功: {DATABASE_URL}")

    # 创建会话工厂
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 创建基类
    Base = declarative_base()

    def init_database():
        """初始化数据库，创建所有表"""
        try:
            from models.user import User
            from models.product import Product
            from models.order import Order
            from models.points import PointsTransaction
            from models.cart import CartItem
            from models.steam_binding import SteamBinding
            from models.invite_code import InviteCode
            
            Base.metadata.create_all(bind=engine)
            logger.info("数据库表创建成功")
        except Exception as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            raise

    def reset_database():
        """重置数据库，删除所有表并重新创建"""
        try:
            Base.metadata.drop_all(bind=engine)
            logger.info("数据库表删除成功")
            init_database()
            logger.info("数据库重置完成")
            return True
        except Exception as e:
            logger.error(f"数据库重置失败: {str(e)}")
            return False

    def get_db():
        """获取数据库会话"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

except Exception as e:
    logger.error(f"数据库配置失败: {str(e)}")
    raise
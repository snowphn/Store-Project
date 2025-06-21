import sqlite3
import os
from datetime import datetime

def reset_database():
    db_path = 'csgo_shop.db'
    
    # 备份现有数据库
    if os.path.exists(db_path):
        backup_path = f'csgo_shop_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        os.rename(db_path, backup_path)
        print(f"已备份数据库到: {backup_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 创建用户表
        cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(128) NOT NULL,
            password_salt VARCHAR(128) NOT NULL,
            points INTEGER DEFAULT 0,
            user_type TEXT DEFAULT 'NORMAL' NOT NULL,
            display_name VARCHAR(100),
            is_admin BOOLEAN DEFAULT 0,
            is_banned BOOLEAN DEFAULT 0,
            avatar VARCHAR(100) DEFAULT 'default_avatar.jpg',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            permissions TEXT DEFAULT '[]',
            invite_code_used VARCHAR(20)
        )
        ''')
        
        # 创建邀请码表
        cursor.execute('''
        CREATE TABLE invite_codes (
            id INTEGER PRIMARY KEY,
            code VARCHAR(20) UNIQUE NOT NULL,
            privilege_type TEXT DEFAULT 'NORMAL' NOT NULL,
            is_used BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            used_at DATETIME,
            used_by_user_id INTEGER,
            FOREIGN KEY (used_by_user_id) REFERENCES users (id)
        )
        ''')
        
        # 创建产品表
        cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            image_url VARCHAR(255),
            category VARCHAR(50),
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME
        )
        ''')
        
        # 创建订单表
        cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            total_points REAL NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            items TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # 创建购物车表
        cursor.execute('''
        CREATE TABLE cart_items (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        ''')
        
        # 创建积分交易表
        cursor.execute('''
        CREATE TABLE points_transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            type VARCHAR(20) NOT NULL,
            description VARCHAR(255),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # 创建Steam绑定表
        cursor.execute('''
        CREATE TABLE steam_bindings (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            steam_id VARCHAR(50) UNIQUE NOT NULL,
            steam_name VARCHAR(100),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        conn.commit()
        print("数据库重置完成！所有表已重新创建。")
        
    except Exception as e:
        print(f"重置数据库时出错: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    reset_database()
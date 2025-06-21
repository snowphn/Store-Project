import sqlite3
import os

def fix_database():
    db_path = 'csgo_shop.db'
    
    if not os.path.exists(db_path):
        print(f"数据库文件 {db_path} 不存在")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查并添加 invite_codes 表的缺失列
        cursor.execute("PRAGMA table_info(invite_codes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'privilege_type' not in columns:
            print("添加 privilege_type 列到 invite_codes 表")
            cursor.execute("ALTER TABLE invite_codes ADD COLUMN privilege_type TEXT DEFAULT 'NORMAL'")
        
        if 'used_by_user_id' not in columns:
            print("添加 used_by_user_id 列到 invite_codes 表")
            cursor.execute("ALTER TABLE invite_codes ADD COLUMN used_by_user_id INTEGER")
        
        # 检查并添加 users 表的缺失列
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_type' not in columns:
            print("添加 user_type 列到 users 表")
            cursor.execute("ALTER TABLE users ADD COLUMN user_type TEXT DEFAULT 'NORMAL'")
        
        if 'display_name' not in columns:
            print("添加 display_name 列到 users 表")
            cursor.execute("ALTER TABLE users ADD COLUMN display_name TEXT")
        
        if 'invite_code_used' not in columns:
            print("添加 invite_code_used 列到 users 表")
            cursor.execute("ALTER TABLE users ADD COLUMN invite_code_used TEXT")
        
        conn.commit()
        print("数据库修复完成！")
        
    except Exception as e:
        print(f"修复数据库时出错: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()
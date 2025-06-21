import sqlite3

db_path = "csgo_shop.db"  # 数据库文件名
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查字段是否已存在
cursor.execute("PRAGMA table_info(users);")
columns = [col[1] for col in cursor.fetchall()]
if "password_salt" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN password_salt VARCHAR(128);")
    print("已成功添加 password_salt 字段！")
else:
    print("password_salt 字段已存在，无需添加。")

conn.commit()
conn.close()
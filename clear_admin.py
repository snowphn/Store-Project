from database.db_init import SessionLocal
from models.user import User

db = SessionLocal()
admin = db.query(User).filter(User.username == "admin").first()
if admin:
    db.delete(admin)
    db.commit()
    print("已删除旧的admin用户")
else:
    print("未找到admin用户")
db.close()
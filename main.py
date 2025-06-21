import sys
import os
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
from views.main_window import MainWindow
from database.db_init import init_database, SessionLocal
from database.db_operations import delete_demo_data
from models.user import User
from utils.password import hash_password
from utils.splash_animation import AnimatedSplashScreen


os.environ['USE_PAYMENT_SIMULATION'] = 'true'

def create_default_admin():
    """创建默认管理员账户"""
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@hurricane.com",
                is_admin=True
            )
            admin.set_password("111")
            db.add(admin)
            db.commit()
            print("✓ 默认管理员创建成功！用户名：admin 密码：111")
        else:
            print("✓ 默认管理员账号已存在")
    except Exception as e:
        print(f"✗ 创建管理员失败：{e}")
        db.rollback()
    finally:
        db.close()

def setup_application():
    """设置应用程序"""
    app = QApplication(sys.argv)
    from utils.language_manager import language_manager
    app.setApplicationName(language_manager.get_text('app_title'))
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Hurricane Team")
    
    # 设置全局字体
    font = QFont("Microsoft YaHei UI", 9)
    app.setFont(font)
    
    return app

def show_splash_screen(app):
    """显示启动画面"""
    splash = AnimatedSplashScreen()
    splash.show()
    splash.start_animations()
    app.processEvents()
    return splash

def main():
    """主函数"""
    print("🚀 Hurricane Community Store 启动中...")
    
    # 设置应用程序
    app = setup_application()
    
    # 显示启动画面
    splash = show_splash_screen(app)
    
    try:
        # 初始化数据库
        splash.update_progress(20, "正在初始化数据库...")
        app.processEvents()
        init_database()
        
        # 创建默认管理员
        splash.update_progress(40, "正在创建默认账户...")
        app.processEvents()
        create_default_admin()
        
        # 清理演示数据
        splash.update_progress(60, "正在清理演示数据...")
        app.processEvents()
        delete_demo_data()
        
        # 创建主窗口
        splash.update_progress(80, "正在加载界面...")
        app.processEvents()
        
        window = MainWindow()
        
        # 完成加载
        splash.update_progress(100, "启动完成！")
        app.processEvents()
        
        # 延迟显示主窗口
        QTimer.singleShot(0, lambda: (
            splash.finish_animation(),
            splash.finish(window),
            window.show()
        ))
        
        print("✓ 应用程序启动成功！")
        
    except Exception as e:
        print(f"✗ 启动失败：{e}")
        splash.close()
        return 1
    
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
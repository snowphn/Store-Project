from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QFrame,
                             QStackedWidget, QPushButton, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from .login_view import LoginView
from .register_view import RegisterView
from .home_view import HomeView
from .cart_view import CartView
from .user_profile_view import UserProfileView
from .admin_view import AdminView
from .csgo_server_view import CSGOServerView
from models.user import User
from database.db_operations import get_user_by_username, create_user
from resources.icons import get_app_icon
from resources.enhanced_styles import (
    get_enhanced_background_style, 
    get_enhanced_content_style,
    get_floating_elements_style,
    create_floating_decorations,
    animate_floating_elements
)
from utils.language_manager import language_manager

class MainWindow(QMainWindow):
    # 语言切换信号
    language_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.floating_decorations = []
        self.floating_animations = []
        self.init_ui()
        self.init_views()
        self.show_login()
    
    def init_ui(self):
        """初始化主窗口UI"""
        self.setWindowTitle(language_manager.get_text('app_title'))
        self.setWindowIcon(get_app_icon())
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)
        
        # 应用增强版样式
        enhanced_style = (
            get_enhanced_background_style() + 
            get_enhanced_content_style() + 
            get_floating_elements_style()
        )
        self.setStyleSheet(enhanced_style)
        
        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建顶部工具栏
        self.create_top_toolbar()
        
        # 创建装饰性背景框架
        self.decorative_frame = QFrame()
        self.decorative_frame.setObjectName("decorative_bg")
        decorative_layout = QVBoxLayout(self.decorative_frame)
        decorative_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建堆叠部件用于切换不同页面
        self.stacked_widget = QStackedWidget()
        decorative_layout.addWidget(self.stacked_widget)
        
        self.main_layout.addWidget(self.decorative_frame)
        
        # 创建浮动装饰元素
        QTimer.singleShot(1000, self.create_decorations)
    
    def create_decorations(self):
        """创建装饰元素"""
        try:
            self.floating_decorations = create_floating_decorations(self.central_widget)
            self.floating_animations = animate_floating_elements(
                self.floating_decorations, self.central_widget
            )
        except Exception as e:
            print(f"创建装饰元素失败: {e}")
    
    def resizeEvent(self, event):
        """窗口大小改变时重新定位装饰元素"""
        super().resizeEvent(event)
        # 重新创建装饰元素以适应新尺寸
        if hasattr(self, 'floating_decorations') and self.floating_decorations:
            QTimer.singleShot(100, self.create_decorations)
    
    def init_views(self):
        """初始化所有视图"""
        self.login_view = LoginView(self)
        self.register_view = RegisterView(self)
        self.home_view = HomeView(self)
        self.cart_view = CartView(self)
        self.profile_view = UserProfileView(self)
        self.admin_view = AdminView(self)
        self.csgo_server_view = CSGOServerView(self)
        
        # 添加视图到堆叠部件
        self.stacked_widget.addWidget(self.login_view)
        self.stacked_widget.addWidget(self.register_view)
        self.stacked_widget.addWidget(self.home_view)
        self.stacked_widget.addWidget(self.cart_view)
        self.stacked_widget.addWidget(self.profile_view)
        self.stacked_widget.addWidget(self.admin_view)
        self.stacked_widget.addWidget(self.csgo_server_view)
    
    def show_login(self):
        """显示登录页面"""
        self.stacked_widget.setCurrentWidget(self.login_view)
    
    def show_register(self):
        """显示注册页面"""
        self.stacked_widget.setCurrentWidget(self.register_view)
    
    def show_home(self):
        """显示商城页面"""
        if self.current_user:
            self.current_user = get_user_by_username(self.current_user.username)
        self.stacked_widget.setCurrentWidget(self.home_view)
        self.home_view.load_products()
    
    def show_cart(self):
        """显示购物车页面"""
        if not self.current_user:
            self.show_warning("请先登录")
            return
        self.stacked_widget.setCurrentWidget(self.cart_view)
        self.cart_view.load_cart_items()
    
    def show_profile(self):
        """显示用户资料页面"""
        if not self.current_user:
            self.show_warning("请先登录")
            return
        self.stacked_widget.setCurrentWidget(self.profile_view)
        self.profile_view.load_user_info()
    
    def show_admin(self):
        """显示管理员页面"""
        if not self.current_user or not self.current_user.is_admin:
            self.show_warning("无权限访问")
            return
        self.stacked_widget.setCurrentWidget(self.admin_view) 
        self.admin_view.load_data()

    def show_csgo_server(self):
        """显示CSGO服务器查询页面"""
        if not self.current_user:
            self.show_warning("请先登录")
            return
        self.stacked_widget.setCurrentWidget(self.csgo_server_view)

    def login(self, username: str, password: str):
        """用户登录"""
        user = get_user_by_username(username)
        if user and user.check_password(password):
            # 检查用户是否被封禁
            if user.is_banned:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("账户被封禁")
                msg_box.setText("您的账户已被封禁，有问题请联系管理员。")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: #ffffff;
                        border-radius: 10px;
                    }
                    QMessageBox QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        font-weight: bold;
                        min-width: 80px;
                    }
                    QMessageBox QPushButton:hover {
                        background-color: #c0392b;
                    }
                """)
                msg_box.exec_()
                return False
            
            self.current_user = user
            self.show_home()
            return True
        return False
    
    def logout(self):
        """用户登出"""
        self.current_user = None
        self.show_login()
    
    def show_warning(self, message: str):
        """显示警告消息"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("提示")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
                border-radius: 10px;
            }
            QMessageBox QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        msg_box.exec_()

    def register(self, username: str, password: str, email: str):
        """用户注册"""
        try:
            user = create_user(username, email, password)
            self.current_user = user
            self.show_home()
            return True, "注册成功"
        except Exception as e:
            return False, f"注册失败: {str(e)}"

    def closeEvent(self, event):
        """关闭窗口事件"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("离别")
        msg_box.setText("你确定要离开我吗?宝宝")
        confirm_button = QPushButton("确定")
        confirm_button.setFixedWidth(189)
        confirm_button.setStyleSheet("background-color: #FF5722; color: white; font-size: 15px; border-radius: 4px;")
        msg_box.addButton(confirm_button, QMessageBox.AcceptRole)
        
        cancel_button = QPushButton("取消")
        cancel_button.setFixedWidth(189)
        cancel_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 15px; border-radius: 4px;")
        msg_box.addButton(cancel_button, QMessageBox.RejectRole)
        
        result = msg_box.exec_()
        if result == QMessageBox.AcceptRole:
            event.accept()
        else:
            event.ignore()
    
    def create_top_toolbar(self):
        """创建顶部工具栏"""
        self.toolbar_frame = QFrame()
        self.toolbar_frame.setFixedHeight(50)
        self.toolbar_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255,255,255,0.9), 
                    stop:1 rgba(255,255,255,0.7));
                border-bottom: 1px solid rgba(0,0,0,0.1);
            }
        """)
        
        toolbar_layout = QHBoxLayout(self.toolbar_frame)
        toolbar_layout.setContentsMargins(20, 5, 20, 5)
        
        # 左侧空白区域
        toolbar_layout.addStretch()
        
        # 语言切换按钮
        self.language_button = QPushButton()
        self.update_language_button_text()
        self.language_button.setFixedSize(120, 35)
        self.language_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 17px;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6fd8, stop:1 #6a4190);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4e5bc6, stop:1 #5e3a7e);
            }
        """)
        self.language_button.clicked.connect(self.toggle_language)
        toolbar_layout.addWidget(self.language_button)
        
        # 将工具栏添加到主布局的顶部
        self.main_layout.insertWidget(0, self.toolbar_frame)
    
    def update_language_button_text(self):
        """更新语言按钮文本"""
        if language_manager.get_current_language() == 'zh':
            self.language_button.setText('🌐 English')
        else:
            self.language_button.setText('🌐 中文')
    
    def toggle_language(self):
        """切换语言"""
        new_language = language_manager.toggle_language()
        self.update_ui_language()
        self.language_changed.emit(new_language)
    
    def update_ui_language(self):
        """更新整个UI的语言"""
        # 更新窗口标题
        self.setWindowTitle(language_manager.get_text('app_title'))
        
        # 更新语言按钮文本
        self.update_language_button_text()
        
        # 更新所有视图的语言
        all_views = [
            self.login_view,
            self.register_view,
            self.home_view,
            self.cart_view,
            self.profile_view,
            self.admin_view,
            self.csgo_server_view
        ]
        
        for view in all_views:
            if hasattr(view, 'update_language'):
                view.update_language()
        
        # 更新当前视图的语言
        current_widget = self.stacked_widget.currentWidget()
        if hasattr(current_widget, 'update_language'):
            current_widget.update_language()
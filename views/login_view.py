from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap
from database.db_operations import verify_user
from utils.password import verify_password
from database.db_init import SessionLocal
from models.user import User
from resources.icons import get_app_icon, get_icon
from utils.language_manager import language_manager

class LoginView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 主布局
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 左侧装饰区域
        left_frame = QFrame()
        left_frame.setFixedWidth(600)
        # 在第25行左右，修改左侧装饰区域背景
        left_frame.setStyleSheet("""
            QFrame {
                background: #f8f9fa;  # 改为浅灰白色
                border-radius: 0;
            }
        """)
        
        left_layout = QVBoxLayout(left_frame)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # 左侧内容
        self.welcome_label = QLabel(language_manager.get_text('switch_to_english') if language_manager.get_current_language() == 'zh' else "欢迎来到")
        self.welcome_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: 300;
                margin-bottom: 10px;
            }
        """)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        
        app_name = QLabel(language_manager.get_text('app_title'))
        app_name.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        app_name.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("您的专属游戏商城")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 18px;
                font-weight: 300;
            }
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        
        left_layout.addWidget(self.welcome_label)
        left_layout.addWidget(app_name)
        left_layout.addWidget(subtitle)
        
        # 右侧登录区域
        right_frame = QFrame()
        right_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 0;
            }
        """)
        
        right_layout = QVBoxLayout(right_frame)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(80, 50, 80, 50)
        
        # 登录表单容器
        form_container = QFrame()
        form_container.setMaximumWidth(400)
        form_container.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 20px;
                padding: 40px;
            }
        """)
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(25)
        
        # 登录标题
        self.login_title = QLabel(language_manager.get_text('login'))
        self.login_title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 30px;
            }
        """)
        self.login_title.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.login_title)
        
        # 用户名输入
        username_container = self.create_input_field(language_manager.get_text('username'), "user")
        self.username_input = username_container.findChild(QLineEdit)
        form_layout.addWidget(username_container)
        
        # 密码输入
        password_container = self.create_input_field(language_manager.get_text('password'), "password", is_password=True)
        self.password_input = password_container.findChild(QLineEdit)
        form_layout.addWidget(password_container)
        
        # 登录按钮
        self.login_button = QPushButton(language_manager.get_text('login_button'))
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #5a67d8, stop:1 #667eea);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #4c51bf, stop:1 #5a67d8);
            }
        """)
        self.login_button.clicked.connect(self.login)
        form_layout.addWidget(self.login_button)
        
        # 注册链接
        register_layout = QHBoxLayout()
        self.register_text = QLabel(language_manager.get_text('no_account_text'))
        self.register_text.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        
        self.register_link = QPushButton(language_manager.get_text('register_now'))
        self.register_link.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #667eea;
                border: none;
                font-size: 14px;
                font-weight: bold;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #5a67d8;
            }
        """)
        self.register_link.clicked.connect(self.show_register)
        
        register_layout.addStretch()
        register_layout.addWidget(self.register_text)
        register_layout.addWidget(self.register_link)
        register_layout.addStretch()
        form_layout.addLayout(register_layout)
        
        right_layout.addWidget(form_container)
        
        # 添加到主布局
        main_layout.addWidget(left_frame)
        main_layout.addWidget(right_frame)
        
        self.setLayout(main_layout)
    
    def create_input_field(self, placeholder, icon_name, is_password=False):
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 添加图标
        icon_label = QLabel()
        icon_label.setPixmap(get_icon(icon_name).pixmap(20, 20))
        layout.addWidget(icon_label)
        
        # 创建输入框
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet("""
            QLineEdit {
                border: none;
                font-size: 14px;
            }
        """)
        if is_password:
            input_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(input_field)
        
        return container
    
    def login(self):
        """登录处理"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.show_message("请输入用户名和密码", "warning")
            return
        
        if self.main_window.login(username, password):
            self.username_input.clear()
            self.password_input.clear()
        else:
            self.show_message("用户名或密码错误", "error")
    
    def show_register(self):
        """显示注册页面"""
        self.main_window.show_register()
    
    def show_message(self, message, msg_type="info"):
        """显示消息"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("提示")
        msg_box.setText(message)
        
        if msg_type == "warning":
            msg_box.setIcon(QMessageBox.Warning)
        elif msg_type == "error":
            msg_box.setIcon(QMessageBox.Critical)
        else:
            msg_box.setIcon(QMessageBox.Information)
        
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
                border-radius: 10px;
            }
            QMessageBox QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #5a67d8;
            }
        """)
        msg_box.exec_()
    
    def update_language(self):
        """更新界面语言"""
        # 更新左侧欢迎文本
        if hasattr(self, 'welcome_label'):
            self.welcome_label.setText(language_manager.get_text('welcome_to'))
        
        # 更新登录标题
        if hasattr(self, 'login_title'):
            self.login_title.setText(language_manager.get_text('login'))
        
        # 更新输入框占位符
        if hasattr(self, 'username_input'):
            self.username_input.setPlaceholderText(language_manager.get_text('username'))
        
        if hasattr(self, 'password_input'):
            self.password_input.setPlaceholderText(language_manager.get_text('password'))
        
        # 更新按钮文本
        if hasattr(self, 'login_button'):
            self.login_button.setText(language_manager.get_text('login_button'))
        
        if hasattr(self, 'register_text'):
            if language_manager.get_current_language() == 'zh':
                self.register_text.setText("还没有账户？")
            else:
                self.register_text.setText("Don't have an account?")
        
        if hasattr(self, 'register_link'):
            if language_manager.get_current_language() == 'zh':
                self.register_link.setText("立即注册")
            else:
                self.register_link.setText("Sign up now")
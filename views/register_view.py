from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QCheckBox, QFrame)
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QIcon, QFont, QPixmap
from database.db_operations import create_user, bind_steam_account, verify_invite_code, use_invite_code
from utils.password import hash_password
from utils.steam_api import SteamAPI
from utils.steam_web import SteamWebLogin
from utils.callback_server import start_callback_server, stop_callback_server, get_callback_params

import re
import webbrowser
from database.db_init import SessionLocal
from models.user import User
from resources.icons import get_app_icon, get_icon
from utils.captcha_generator import CaptchaGenerator
from utils.language_manager import language_manager

class RegisterView(QWidget):
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.steam_api = SteamAPI()
        self.steam_web = SteamWebLogin()
        self.callback_server = None
        self.callback_timer = None
        
        # 自定义验证码
        self.captcha_generator = CaptchaGenerator()
        self.current_captcha_code = None
        self.captcha_verified = False
        
        self.setWindowIcon(get_app_icon())
        self.init_ui()
    

    def _add_captcha_section(self, layout):
        """添加图片验证码区域"""
        captcha_layout = QVBoxLayout()
        captcha_layout.setSpacing(10)
        
        # 验证码标题
        captcha_label = QLabel("图片验证码")
        captcha_label.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)
        captcha_layout.addWidget(captcha_label)
        
        # 验证码图片和输入框容器
        captcha_container = QFrame()
        captcha_container.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        container_layout = QHBoxLayout(captcha_container)
        container_layout.setSpacing(15)
        
        # 验证码图片
        self.captcha_image_label = QLabel()
        self.captcha_image_label.setFixedSize(120, 50)
        self.captcha_image_label.setStyleSheet("""
            QLabel {
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
            }
        """)
        self.captcha_image_label.mousePressEvent = self.refresh_captcha
        container_layout.addWidget(self.captcha_image_label)
        
        # 右侧布局（输入框和刷新按钮）
        right_layout = QVBoxLayout()
        
        # 验证码输入框
        self.captcha_input = QLineEdit()
        self.captcha_input.setPlaceholderText("请输入图片中的4位数字")
        self.captcha_input.setMaxLength(4)
        self.captcha_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
            }
        """)
        self.captcha_input.textChanged.connect(self.validate_captcha_input)
        right_layout.addWidget(self.captcha_input)
        
        # 刷新按钮
        refresh_button = QPushButton("刷新验证码")
        refresh_button.setStyleSheet("""
            QPushButton {
                background: #f8f9fa;
                color: #333;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #e9ecef;
                border: 1px solid #adb5bd;
            }
        """)
        refresh_button.clicked.connect(self.refresh_captcha)
        right_layout.addWidget(refresh_button)
        
        container_layout.addLayout(right_layout)
        captcha_layout.addWidget(captcha_container)
        
        # 验证状态标签
        self.captcha_status_label = QLabel(language_manager.get_text('enter_captcha'))
        self.captcha_status_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
                padding: 5px;
                background: #f8f9fa;
                border-radius: 4px;
            }
        """)
        captcha_layout.addWidget(self.captcha_status_label)
        
        layout.addLayout(captcha_layout)
        
        # 生成初始验证码
        self.refresh_captcha()
    
    def refresh_captcha(self, event=None):
        """刷新验证码"""
        self.current_captcha_code, pixmap = self.captcha_generator.generate_captcha()
        self.captcha_image_label.setPixmap(pixmap)
        self.captcha_input.clear()
        self.captcha_verified = False
        self.update_captcha_status(language_manager.get_text('enter_captcha'), "info")
        print(f"新验证码: {self.current_captcha_code}")  # 调试用，生产环境应删除
    
    def validate_captcha_input(self):
        """验证用户输入的验证码"""
        user_input = self.captcha_input.text().strip()
        
        if len(user_input) == 4:
            if user_input == self.current_captcha_code:
                self.captcha_verified = True
                self.update_captcha_status(language_manager.get_text('captcha_success'), "success")
            else:
                self.captcha_verified = False
                self.update_captcha_status(language_manager.get_text('captcha_error'), "error")
        else:
            self.captcha_verified = False
            if user_input:
                self.update_captcha_status(language_manager.get_text('enter_4_digits'), "warning")
            else:
                self.update_captcha_status(language_manager.get_text('enter_captcha'), "info")
    
    def update_captcha_status(self, message, status_type):
        """更新验证码状态显示"""
        self.captcha_status_label.setText(message)
        
        if status_type == "success":
            style = """
                QLabel {
                    color: #4CAF50;
                    font-size: 12px;
                    padding: 5px;
                    background: #e8f5e8;
                    border-radius: 4px;
                    font-weight: bold;
                }
            """
        elif status_type == "error":
            style = """
                QLabel {
                    color: #f44336;
                    font-size: 12px;
                    padding: 5px;
                    background: #ffebee;
                    border-radius: 4px;
                }
            """
        elif status_type == "warning":
            style = """
                QLabel {
                    color: #ff9800;
                    font-size: 12px;
                    padding: 5px;
                    background: #fff3e0;
                    border-radius: 4px;
                }
            """
        else:  # info
            style = """
                QLabel {
                    color: #666;
                    font-size: 12px;
                    padding: 5px;
                    background: #f8f9fa;
                    border-radius: 4px;
                }
            """
        
        self.captcha_status_label.setStyleSheet(style)
    

    def init_ui(self):
        """初始化UI"""
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 设置整体样式
        self.setStyleSheet(self._get_styles())
        
        # 创建内容框架
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_frame.setMinimumWidth(450)
        content_frame.setMaximumWidth(450)
        
        # 内容布局
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(20)
        
        # 添加标题区域
        self._add_title_section(content_layout)
        
        # 添加输入字段区域
        self._add_input_fields(content_layout)
        
        # 添加图片验证码区域
        self._add_captcha_section(content_layout)
        
        # 添加Steam绑定区域
        self._add_steam_section(content_layout)
        
        # 添加按钮区域
        self._add_button_section(content_layout)
        
        # 将内容框架居中
        center_layout = QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(content_frame, 0, Qt.AlignCenter)
        center_layout.addStretch()
        
        main_layout.addLayout(center_layout)
        self.setLayout(main_layout)
    
    def _get_styles(self):
        """获取样式表"""
        return """
            QWidget {
                background: #f8f9fa;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            }
            QFrame#content_frame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                min-width: 450px;
                max-width: 450px;
            }
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #333;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background: #fafafa;
            }
            QLineEdit:hover {
                border: 2px solid #b0b0b0;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6fd8, stop:1 #6a4190);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4e5bc6, stop:1 #5e397e);
            }
            QPushButton#register_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
            }
            QPushButton#register_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #45a049, stop:1 #3d8b40);
            }
            QPushButton#steam_btn {
                background: rgba(255, 255, 255, 0.95);
                color: #333;
                border: 2px solid #e0e0e0;
            }
            QPushButton#steam_btn:hover {
                background: rgba(255, 255, 255, 1.0);
                border: 2px solid #667eea;
            }
            QCheckBox {
                color: #333;
                font-size: 14px;
                spacing: 8px;
                background: #f8f9fa;
                padding: 8px;
                border-radius: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #ddd;
                border-radius: 4px;
                background: white;
            }
            QCheckBox::indicator:checked {
                background: #667eea;
                border: 2px solid #667eea;
            }
            QCheckBox::indicator:checked:hover {
                background: #5a6fd8;
            }
        """
    
    def _add_title_section(self, layout):
        """添加标题区域"""
        title_layout = QVBoxLayout()
        title_layout.setSpacing(10)
        
        # 图标
        icon_label = QLabel()
        icon_label.setPixmap(get_icon("register").pixmap(48, 48))
        icon_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(icon_label)
        
        # 标题
        self.title = QLabel(language_manager.get_text('register'))
        title_font = QFont("Microsoft YaHei", 24, QFont.Bold)
        self.title.setFont(title_font)
        self.title.setStyleSheet("color: #333; margin: 10px 0; background: #f8f9fa; padding: 10px; border-radius: 8px;")
        self.title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.title)
        
        layout.addLayout(title_layout)
    
    def _add_input_fields(self, layout):
        """添加输入字段区域"""
        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(15)
        
        # 创建输入字段
        self.username_input = self._create_input_field(language_manager.get_text('username'), "user")
        self.email_input = self._create_input_field(language_manager.get_text('email'), "mail")
        self.password_input = self._create_input_field(language_manager.get_text('password'), "password", is_password=True)
        self.invite_input = self._create_input_field(language_manager.get_text('invite_code_optional'), "invite")
        
        fields_layout.addWidget(self.username_input)
        fields_layout.addWidget(self.email_input)
        fields_layout.addWidget(self.password_input)
        fields_layout.addWidget(self.invite_input)
        
        layout.addLayout(fields_layout)
    

    

    

    
    def _add_steam_section(self, layout):
        """添加Steam绑定区域"""
        steam_layout = QVBoxLayout()
        steam_layout.setSpacing(10)
        
        self.steam_checkbox = QCheckBox("绑定Steam账号")
        self.steam_checkbox.stateChanged.connect(self.toggle_steam_bind)
        steam_layout.addWidget(self.steam_checkbox)
        
        self.steam_bind_button = QPushButton("使用Steam账号登录")
        self.steam_bind_button.setObjectName("steam_btn")
        self.steam_bind_button.setVisible(False)
        self.steam_bind_button.clicked.connect(self.handle_steam_login)
        steam_layout.addWidget(self.steam_bind_button)
        
        layout.addLayout(steam_layout)
    
    def _add_button_section(self, layout):
        """添加按钮区域"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.register_button = QPushButton(language_manager.get_text('confirm_register'))
        self.register_button.setObjectName("register_btn")
        self.register_button.setIcon(get_icon("checkmark"))
        self.register_button.clicked.connect(self.register)
        button_layout.addWidget(self.register_button)
        
        self.back_button = QPushButton(language_manager.get_text('back_to_login'))
        self.back_button.setIcon(get_icon("back"))
        self.back_button.clicked.connect(self.main_window.show_login)
        button_layout.addWidget(self.back_button)
        
        layout.addLayout(button_layout)
    
    def update_language(self):
        """更新注册视图的语言"""
        # 更新标题
        self.title.setText(language_manager.get_text('register'))
        
        # 更新按钮文本
        self.register_button.setText(language_manager.get_text('confirm_register'))
        self.back_button.setText(language_manager.get_text('back_to_login'))
        
        # 更新输入框占位符
        username_input = self.username_input.findChild(QLineEdit)
        if username_input:
            username_input.setPlaceholderText(language_manager.get_text('username'))
            
        email_input = self.email_input.findChild(QLineEdit)
        if email_input:
            email_input.setPlaceholderText(language_manager.get_text('email'))
            
        password_input = self.password_input.findChild(QLineEdit)
        if password_input:
            password_input.setPlaceholderText(language_manager.get_text('password'))
            
        invite_input = self.invite_input.findChild(QLineEdit)
        if invite_input:
            invite_input.setPlaceholderText(language_manager.get_text('invite_code_optional'))
    
    def _create_input_field(self, placeholder, icon_name, is_password=False):
        """创建输入字段"""
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
    
    def get_input_value(self, container):
        """获取输入框的值"""
        layout = container.layout()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                return widget.text().strip()
        return ""
    
    def clear_input(self, container):
        """清空输入框"""
        layout = container.layout()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                widget.clear()
    
    def toggle_steam_bind(self, state):
        """切换Steam绑定按钮的显示状态"""
        self.steam_bind_button.setVisible(state == Qt.Checked)
        self.adjustSize()
        QTimer.singleShot(0, self.recenter_content)
        if self.parent():
            self.parent().adjustSize()
    
    def recenter_content(self):
        """重新居中内容框架"""
        main_layout = self.layout()
        if main_layout and main_layout.count() > 0:
            center_layout_item = main_layout.itemAt(0)
            if center_layout_item and hasattr(center_layout_item, 'layout'):
                center_layout = center_layout_item.layout()
                if center_layout:
                    center_layout.invalidate()
                    center_layout.activate()
        self.update()
        self.repaint()
    
    def handle_steam_login(self):
        """处理Steam登录"""
        try:
            # 启动回调服务器
            self.callback_server = start_callback_server()
            
            # 生成回调URL
            return_url = "http://localhost:8000/steam/callback"
            
            # 获取Steam登录URL
            login_url = self.steam_web.get_login_url(return_url)
            
            # 打开浏览器进行Steam登录
            webbrowser.open(login_url)
            
            # 显示等待提示
            QMessageBox.information(self, "提示", "请在浏览器中完成Steam登录授权")
            
            # 启动定时器检查回调
            self.callback_timer = QTimer()
            self.callback_timer.timeout.connect(self.check_steam_callback)
            self.callback_timer.start(1000)  # 每秒检查一次
        except Exception as e:
            self.show_message("错误", f"Steam登录失败: {str(e)}", "error")
    
    def check_steam_callback(self):
        """检查Steam登录回调"""
        try:
            params = get_callback_params()
            if params:
                # 停止定时器和服务器
                self.callback_timer.stop()
                stop_callback_server(self.callback_server)
                
                # 处理回调
                self.handle_steam_callback(params)
        except Exception as e:
            self.show_message("错误", f"检查Steam回调失败: {str(e)}", "error")
    
    def handle_steam_callback(self, params: dict):
        """处理Steam登录回调"""
        try:
            # 验证Steam登录
            steam_info = self.steam_web.verify_login(params)
            if not steam_info:
                self.show_message("错误", "Steam登录验证失败", "error")
                return
            
            # 保存Steam信息用于注册
            self.steam_info = steam_info
            self.show_message("成功", f"Steam账号绑定成功: {steam_info['name']}")
        except Exception as e:
            self.show_message("错误", f"处理Steam回调失败: {str(e)}", "error")
    
    def validate_email(self, email):
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "邮箱格式不正确"
        return True, "邮箱验证通过"
    
    def register(self):
        """处理注册"""
        try:
            username = self.get_input_value(self.username_input)
            email = self.get_input_value(self.email_input)
            password = self.get_input_value(self.password_input)
            invite_code = self.get_input_value(self.invite_input) or None  # 空字符串转为None
            
            # 验证输入
            if not username or not email or not password:
                self.show_message("警告", "请填写所有必填字段", "warning")
                return
            
            if len(password) < 6:
                self.show_message("错误", "密码长度不能少于6位", "error")
                return
            
            is_valid, error_msg = self.validate_email(email)
            if not is_valid:
                self.show_message("错误", error_msg, "error")
                return
            
            # 验证图片验证码
            if not self.captcha_verified:
                self.show_message("错误", "请完成图片验证码验证", "error")
                return
            
            # 验证邀请码（如果提供）
            if invite_code and not verify_invite_code(invite_code):
                self.show_message("错误", "邀请码无效或已被使用", "error")
                return
            
            try:
                # 创建用户（包含邀请码处理）
                success, message = create_user(username, email, password, invite_code)
                
                if not success:
                    self.show_message("错误", message, "error")
                    return
                    
                user = message  # 成功时返回用户对象
                
                # 绑定Steam账号（如果选择了）
                if self.steam_checkbox.isChecked() and hasattr(self, 'steam_info'):
                    bind_steam_account(user.id, self.steam_info['steam_id'], self.steam_info['name'])
                
                # 刷新后台管理界面
                if hasattr(self.main_window, 'admin_view'):
                    self.main_window.admin_view.load_users()
                    self.main_window.admin_view.load_invite_codes()
                
                self.show_message("成功", "注册成功！")
                self.main_window.show_login()
                
            except ValueError as e:
                self.show_message("错误", str(e), "error")
            
        except Exception as e:
            self.show_message("错误", f"注册失败: {str(e)}", "error")
    
    def show_message(self, title, message, msg_type="info"):
        """显示消息框"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        # 根据消息类型设置不同的图标
        if msg_type == "error":
            msg_box.setIcon(QMessageBox.Critical)
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setIcon(QMessageBox.Information)
        
        msg_box.setStyleSheet("""
            QMessageBox {
                background: white;
                color: #333;
            }
            QMessageBox QPushButton {
                background: #667eea;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 14px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: #5a6fd8;
            }
        """)
        msg_box.exec_()
    
    def clear_inputs(self):
        """清空输入框"""
        self.clear_input(self.username_input)
        self.clear_input(self.email_input)
        self.clear_input(self.password_input)
        self.clear_input(self.invite_input)
        self.steam_checkbox.setChecked(False)
        if hasattr(self, 'steam_info'):
            delattr(self, 'steam_info')
        
        # 重置验证码验证状态
        self.captcha_verified = False
        if hasattr(self, 'captcha_input'):
            self.captcha_input.clear()
        if hasattr(self, 'captcha_status_label'):
            self.update_captcha_status("请输入图片中的验证码", "info")
        # 刷新验证码
        if hasattr(self, 'captcha_generator'):
            self.refresh_captcha()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止回调服务器和定时器
        if self.callback_server:
            stop_callback_server(self.callback_server)
        if self.callback_timer:
            self.callback_timer.stop()
        event.accept()
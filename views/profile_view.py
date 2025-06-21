from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QMessageBox,
                             QLineEdit, QGridLayout, QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont, QIcon, QImage
from database.db_operations import (get_user_by_id, update_user_info, 
                                  get_user_points_transactions, get_steam_binding, 
                                  unbind_steam_account, update_user_avatar)
from database.db_init import SessionLocal
from utils.password import hash_password
from models.user import User
from utils.steam_web import SteamWebLogin
from utils.callback_server import start_callback_server, stop_callback_server, get_callback_params
from utils.image_utils import qimage_to_pixmap
from resources.icons import get_app_icon, get_icon
from utils.language_manager import language_manager
import webbrowser
import os
import shutil

class ProfileView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.steam_web = SteamWebLogin()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Microsoft YaHei', Arial, sans-serif;
            }
            QFrame[card="true"] {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fff, stop:1 #e3eafc);
                border-radius: 18px;
                box-shadow: 0 4px 24px rgba(33,150,243,0.08);
                margin: 16px 0;
                padding: 18px 24px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2196F3, stop:1 #21CBF3);
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1976D2, stop:1 #00bcd4);
            }
            QLabel[title="true"] {
                font-size: 22px;
                font-weight: bold;
                color: #222;
                margin-bottom: 18px;
            }
            QLabel[desc="true"] {
                color: #666;
                font-size: 15px;
            }
            QLabel[points="true"] {
                color: #4CAF50;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        # 顶部导航栏
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(16)
        nav_icon = QLabel()
        nav_icon.setPixmap(get_icon("user").pixmap(32, 32))
        nav_layout.addWidget(nav_icon)
        nav_layout.addStretch()
        back_button = QPushButton(get_icon("back"), language_manager.get_text('back_to_shop'))
        back_button.clicked.connect(self.main_window.show_home)
        nav_layout.addWidget(back_button)
        logout_button = QPushButton(get_icon("logout"), language_manager.get_text('logout'))
        logout_button.clicked.connect(self.main_window.logout)
        nav_layout.addWidget(logout_button)
        layout.addLayout(nav_layout)
        # 个人信息卡片
        info_frame = QFrame()
        info_frame.setProperty("card", True)
        info_layout = QVBoxLayout()
        # 头像区域
        avatar_container = QWidget()
        avatar_container_layout = QVBoxLayout()
        
        # 头像显示
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(200, 200)
        self.avatar_label.setStyleSheet("""
            QLabel {
                border: 2px solid #e0e0e0;
                border-radius: 100px;
                background-color: #f8f9fa;
            }
        """)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.load_avatar()
        
        # 更换头像按钮
        change_avatar_btn = QPushButton(language_manager.get_text('change_avatar'))
        change_avatar_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
            QPushButton:pressed {
                background-color: #219a52;
            }
        """)
        change_avatar_btn.clicked.connect(self.change_avatar)
        
        avatar_container_layout.addWidget(self.avatar_label, alignment=Qt.AlignCenter)
        avatar_container_layout.addWidget(change_avatar_btn, alignment=Qt.AlignCenter)
        avatar_container.setLayout(avatar_container_layout)
        info_layout.addWidget(avatar_container)
        # 用户信息
        userinfo_layout = QVBoxLayout()
        self.username_label = QLabel()
        self.username_label.setProperty("title", True)
        userinfo_layout.addWidget(self.username_label)
        self.email_label = QLabel()
        self.email_label.setProperty("desc", True)
        userinfo_layout.addWidget(self.email_label)
        self.points_label = QLabel()
        self.points_label.setProperty("points", True)
        userinfo_layout.addWidget(self.points_label)
        # Steam绑定状态和按钮
        steam_layout = QHBoxLayout()
        self.steam_status_label = QLabel()
        self.steam_status_label.setProperty("desc", True)
        steam_layout.addWidget(self.steam_status_label)
        self.steam_button = QPushButton()
        self.steam_button.setStyleSheet("background-color: #171a21; color: white; border-radius: 6px;")
        self.steam_button.clicked.connect(self.handle_steam_action)
        steam_layout.addWidget(self.steam_button)
        userinfo_layout.addLayout(steam_layout)
        info_layout.addLayout(userinfo_layout)
        info_frame.setLayout(info_layout)
        layout.addWidget(info_frame)
        # 编辑信息卡片
        edit_frame = QFrame()
        edit_frame.setProperty("card", True)
        edit_layout = QVBoxLayout()
        form_layout = QGridLayout()
        form_layout.addWidget(self.create_icon_label("user", language_manager.get_text('new_username') + ":"), 0, 0)
        self.new_username = QLineEdit()
        form_layout.addWidget(self.new_username, 0, 1)
        form_layout.addWidget(self.create_icon_label("mail", language_manager.get_text('new_email') + ":"), 1, 0)
        self.new_email = QLineEdit()
        form_layout.addWidget(self.new_email, 1, 1)
        form_layout.addWidget(self.create_icon_label("password", language_manager.get_text('new_password') + ":"), 2, 0)
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setStyleSheet("lineedit-password-character: '·'; color: #222; font-size: 18px;")
        form_layout.addWidget(self.new_password, 2, 1)
        edit_layout.addLayout(form_layout)
        save_button = QPushButton(get_icon("save"), language_manager.get_text('save_changes'))
        save_button.clicked.connect(self.save_changes)
        edit_layout.addWidget(save_button)
        edit_frame.setLayout(edit_layout)
        layout.addWidget(edit_frame)
        # 积分记录卡片
        points_frame = QFrame()
        points_frame.setProperty("card", True)
        points_layout = QVBoxLayout()
        points_title = QLabel(language_manager.get_text('points_records'))
        points_title.setProperty("title", True)
        points_layout.addWidget(points_title)
        self.points_list = QScrollArea()
        self.points_list.setWidgetResizable(True)
        self.points_list.setStyleSheet("border: none; background: transparent;")
        self.points_content = QWidget()
        self.points_content_layout = QVBoxLayout()
        self.points_content.setLayout(self.points_content_layout)
        self.points_list.setWidget(self.points_content)
        points_layout.addWidget(self.points_list)
        points_frame.setLayout(points_layout)
        layout.addWidget(points_frame)
        layout.addStretch()
        self.setLayout(layout)

    def create_icon_label(self, icon_name, text):
        """Create label with icon"""
        label = QLabel()
        label.setPixmap(get_icon(icon_name).pixmap(20, 20))
        label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 14px;
            }
        """)
        label.setText(text)
        return label

    def load_avatar(self):
        if self.main_window.current_user is None:
            return
        avatar_data = self.main_window.current_user.get_avatar()
        if avatar_data:
            image = QImage.fromData(avatar_data)
            pixmap = qimage_to_pixmap(image, (200, 200))
            self.avatar_label.setPixmap(pixmap)
        else:
            # 设置默认头像
            self.avatar_label.setText(language_manager.get_text('no_avatar'))

    def change_avatar(self):
        """Change avatar"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            language_manager.get_text('select_avatar'),
            "",
            language_manager.get_text('image_files')
        )
        
        if file_name:
            try:
                # 读取图片
                image = QImage(file_name)
                if image.isNull():
                    raise Exception(language_manager.get_text('cannot_load_image'))
                    
                # 更新头像
                self.main_window.current_user.set_avatar(image)
                
                # 保存到数据库
                db = SessionLocal()
                try:
                    db.commit()
                    self.load_avatar()
                    QMessageBox.information(self, language_manager.get_text('success'), language_manager.get_text('avatar_update_success'))
                except Exception as e:
                    db.rollback()
                    QMessageBox.warning(self, language_manager.get_text('error'), f"{language_manager.get_text('save_avatar_failed')}: {str(e)}")
                finally:
                    db.close()
                    
            except Exception as e:
                QMessageBox.warning(self, language_manager.get_text('error'), f"{language_manager.get_text('update_avatar_failed')}: {str(e)}")

    def load_user_info(self):
        """Load user information"""
        session = SessionLocal()
        try:
            user = session.query(User).filter_by(id=self.main_window.current_user.id).first()
            if user:
                self.username_label.setText(f"{language_manager.get_text('username')}: {user.username}")
                self.email_label.setText(f"{language_manager.get_text('email')}: {user.email}")
                self.points_label.setText(f"{language_manager.get_text('points')}: {user.points}")
                
                # 更新头像显示
                self.main_window.current_user = user
                self.load_avatar()
                
                # 检查Steam绑定状态
                steam_binding = get_steam_binding(user.id)
                if steam_binding:
                    self.steam_status_label.setText(f"{language_manager.get_text('steam_account')}: {steam_binding.steam_name}")
                    self.steam_button.setText(language_manager.get_text('unbind_steam'))
                else:
                    self.steam_status_label.setText(language_manager.get_text('not_bound_steam'))
                    self.steam_button.setText(language_manager.get_text('bind_steam'))
                
                # 加载积分记录
                self.load_points_history(user.id)
                
                # 清空编辑框
                self.new_username.clear()
                self.new_email.clear()
                self.new_password.clear()
        finally:
            session.close()
            
    def load_points_history(self, user_id):
        """Load points history records"""
        # 清空现有记录
        for i in reversed(range(self.points_content_layout.count())): 
            self.points_content_layout.itemAt(i).widget().setParent(None)
            
        # 获取积分记录
        transactions = get_user_points_transactions(user_id)
        
        # 显示记录
        for transaction in transactions:
            record = QFrame()
            record.setStyleSheet("""
                QFrame {
                    background-color: #1e1e1e;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 5px;
                }
            """)
            
            record_layout = QHBoxLayout()
            
            # 交易类型
            type_label = QLabel(transaction.transaction_type)
            type_label.setStyleSheet("color: #ffffff;")
            
            # 积分变化
            points_label = QLabel(f"{'+' if transaction.points > 0 else ''}{transaction.points}")
            points_label.setStyleSheet("""
                color: #4CAF50;
                font-weight: bold;
            """ if transaction.points > 0 else """
                color: #f44336;
                font-weight: bold;
            """)
            
            # 时间
            time_label = QLabel(transaction.created_at.strftime("%Y-%m-%d %H:%M"))
            time_label.setStyleSheet("color: #888888;")
            
            record_layout.addWidget(type_label)
            record_layout.addWidget(points_label)
            record_layout.addStretch()
            record_layout.addWidget(time_label)
            
            record.setLayout(record_layout)
            self.points_content_layout.addWidget(record)
        
    def handle_steam_action(self):
        """Handle Steam bind/unbind operations"""
        if self.steam_button.text() == language_manager.get_text('bind_steam'):
            self.handle_steam_bind()
        else:
            self.handle_steam_unbind()
    
    def handle_steam_bind(self):
        """Handle Steam binding"""
        try:
            # 启动回调服务器
            self.callback_server = start_callback_server()
            if not self.callback_server:
                QMessageBox.warning(self, language_manager.get_text('error'), language_manager.get_text('callback_server_failed'))
                return
            
            # 生成回调URL
            return_url = "http://localhost:8000/steam/callback"
            
            # 获取Steam登录URL
            login_url = self.steam_web.get_login_url(return_url)
            
            # 打开浏览器进行Steam登录
            webbrowser.open(login_url)
            
            # 显示等待提示
            QMessageBox.information(self, language_manager.get_text('info'), language_manager.get_text('complete_steam_auth'))
            
            # 启动定时器检查回调
            self.callback_timer = QTimer()
            self.callback_timer.timeout.connect(self.check_steam_callback)
            self.callback_timer.start(1000)  # 每秒检查一次
        except Exception as e:
            QMessageBox.warning(self, language_manager.get_text('error'), f"{language_manager.get_text('steam_bind_failed')}: {str(e)}")
    
    def handle_steam_unbind(self):
        """Handle Steam unbinding"""
        reply = QMessageBox.question(
            self, language_manager.get_text('confirm_unbind'),
            language_manager.get_text('confirm_unbind_steam'),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if unbind_steam_account(self.main_window.current_user.id):
                QMessageBox.information(self, language_manager.get_text('success'), language_manager.get_text('steam_unbound'))
                self.load_user_info()  # 重新加载用户信息
            else:
                QMessageBox.warning(self, language_manager.get_text('error'), language_manager.get_text('unbind_failed'))
    
    def check_steam_callback(self):
        """Check Steam login callback"""
        try:
            params = get_callback_params()
            if params:
                # 停止定时器和服务器
                self.callback_timer.stop()
                stop_callback_server(self.callback_server)
                
                # 处理回调
                self.handle_steam_callback(params)
        except Exception as e:
            print(f"Check Steam callback failed: {str(e)}")
    
    def handle_steam_callback(self, params: dict):
        """Handle Steam login callback"""
        print("[DEBUG] Steam callback params:", params)
        try:
            # 验证Steam登录
            steam_info = self.steam_web.verify_login(params)
            print("[DEBUG] verify_login returned:", steam_info)
            if not steam_info:
                QMessageBox.warning(self, language_manager.get_text('error'), language_manager.get_text('steam_login_verify_failed'))
                return
            # 绑定Steam账号
            result = bind_steam_account(
                self.main_window.current_user.id,
                steam_info['steam_id'],
                steam_info['name']
            )
            print("[DEBUG] bind_steam_account result:", result)
            if result:
                QMessageBox.information(self, language_manager.get_text('success'), f"{language_manager.get_text('steam_bind_success')}: {steam_info['name']}")
                self.load_user_info()  # 重新加载用户信息
            else:
                QMessageBox.warning(self, language_manager.get_text('error'), language_manager.get_text('bind_failed'))
        except Exception as e:
            print("[DEBUG] Handle Steam callback exception:", str(e))
            QMessageBox.warning(self, language_manager.get_text('error'), f"{language_manager.get_text('handle_steam_callback_failed')}: {str(e)}")
    
    def validate_email(self, email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def save_changes(self):
        """Save user information changes"""
        session = SessionLocal()
        try:
            user = session.query(User).filter_by(id=self.main_window.current_user.id).first()
            if not user:
                QMessageBox.warning(self, language_manager.get_text('error'), language_manager.get_text('user_not_exist'))
                return
            # 获取新值
            new_username = self.new_username.text().strip()
            new_email = self.new_email.text().strip()
            new_password = self.new_password.text()
            # 检查是否有修改
            if not any([new_username, new_email, new_password]):
                QMessageBox.information(self, language_manager.get_text('info'), language_manager.get_text('no_changes_to_save'))
                return
            # 校验邮箱格式
            if new_email and not self.validate_email(new_email):
                QMessageBox.warning(self, language_manager.get_text('error'), language_manager.get_text('invalid_email_format'))
                return
            # 更新用户信息
            if new_username:
                user.username = new_username
            if new_email:
                user.email = new_email
            if new_password:
                user.set_password(new_password)
            session.commit()
            # 更新显示
            self.load_user_info()
            QMessageBox.information(self, language_manager.get_text('success'), language_manager.get_text('profile_update_success'))
        except Exception as e:
            session.rollback()
            QMessageBox.warning(self, language_manager.get_text('error'), f"{language_manager.get_text('save_failed')}: {str(e)}")
        finally:
            session.close()

    def closeEvent(self, event):
        """Window close event"""
        # 停止回调服务器和定时器
        if self.callback_server:
            stop_callback_server(self.callback_server)
        if self.callback_timer:
            self.callback_timer.stop()
        event.accept()
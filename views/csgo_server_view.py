from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QFrame,
                             QScrollArea, QMessageBox, QProgressBar, QSpinBox,
                             QComboBox, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QBrush, QLinearGradient, QColor
from utils.csgo_server import CSGOServer
import threading
from resources.icons import get_app_icon, get_icon
from utils.language_manager import language_manager

class ServerQueryThread(QThread):
    """Server query thread"""
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, address):
        super().__init__()
        self.address = address
    
    def run(self):
        try:
            # 修复：正确解包address元组为ip和port参数
            if isinstance(self.address, tuple) and len(self.address) == 2:
                ip, port = self.address
                server = CSGOServer(ip, port)
            elif isinstance(self.address, str):
                # 如果是字符串，使用from_address_string方法
                server = CSGOServer.from_address_string(self.address)
            else:
                raise ValueError(f"无效的地址格式: {self.address}")
                
            result = server.get_server_info()
            if result:
                self.result_ready.emit(result)
            else:
                self.error_occurred.emit(language_manager.get_text('server_connection_failed'))
        except Exception as e:
            self.error_occurred.emit(f"查询失败: {str(e)}")

class CSGOServerView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.query_thread = None
        self.server_list = []  # 存储添加的服务器列表
        
        # 添加固定的Hurricane服务器（不可删除）
        self.init_default_servers()
        self.init_ui()
    
    def init_default_servers(self):
        """初始化默认的Hurricane服务器列表"""
        self.default_servers = [
            {
                'name': 'Hurricane鸟狙魔怔服',
                'ip': '180.188.21.76',
                'port': 27099,
                'type': language_manager.get_text('competitive_server'),
                'description': 'Hurricane官方鸟狙魔怔服服务器',
                'status': language_manager.get_text('not_queried'),
                'is_custom': True,
                'is_default': True  # 标记为默认服务器，不可删除
            },
            {
                'name': 'Hurricane干拉服',
                'ip': '180.188.21.76',
                'port': 27016,
                'type': language_manager.get_text('competitive_server'), 
                'description': 'Hurricane官方干拉服务器',
                'status': language_manager.get_text('not_queried'),
                'is_custom': True,
                'is_default': True
            },
            {
                'name': 'Hurricane鸟狙干拉服',
                'ip': '180.188.21.76',
                'port': 27001,
                'type': language_manager.get_text('competitive_server'),
                'description': 'Hurricane官方鸟狙干拉服务器', 
                'status': language_manager.get_text('not_queried'),
                'is_custom': True,
                'is_default': True
            },
            {
                'name': 'Hurricane鸟狙爆头服',
                'ip': '180.188.21.76',
                'port': 27030,
                'type': '竞技服务器',
                'description': 'Hurricane官方鸟狙爆头服务器',
                'status': language_manager.get_text('not_queried'), 
                'is_custom': True,
                'is_default': True
            },
            {
                'name': 'Hurricane大厅服',
                'ip': '180.188.21.76',
                'port': 27015,
                'type': language_manager.get_text('casual_server'),
                'description': 'Hurricane官方大厅服',
                'status': language_manager.get_text('not_queried'),
                'is_custom': True, 
                'is_default': True
            }
        ]
        
        # 将默认服务器添加到服务器列表
        self.server_list.extend(self.default_servers)
        # 移除这里的 self.init_ui() 调用，避免重复初始化

    def init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 应用增强样式
        self.setStyleSheet("""
            QWidget {
                background: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2d3748;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 10px;
                background: rgba(255,255,255,0.8);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #4a5568;
                background: rgba(255,255,255,0.9);
                border-radius: 6px;
            }
            QLineEdit, QTextEdit, QSpinBox, QComboBox {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                background: rgba(255,255,255,0.9);
                color: #2d3748;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
                border-color: #667eea;
                background: white;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a67d8, stop:1 #6b46c1);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4c51bf, stop:1 #553c9a);
            }
            QPushButton#add_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #48bb78, stop:1 #38a169);
            }
            QPushButton#add_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #38a169, stop:1 #2f855a);
            }
            QPushButton#back_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
            }
            QPushButton#back_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #21618c);
            }
            QLabel {
                color: #4a5568;
                font-size: 13px;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QFrame#nav_frame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 0px;
                min-height: 60px;
                max-height: 60px;
            }
            QLabel#title_label {
                color: black;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
            }
            QFrame#content_frame {
                background: transparent;
            }
        """)
        
        # 导航栏
        nav_frame = QFrame()
        nav_frame.setObjectName("nav_frame")
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(20, 0, 20, 0)
        
        # 返回按钮
        back_button = QPushButton(get_icon("back"), language_manager.get_text('back'))
        back_button.setObjectName("back_button")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        back_button.clicked.connect(self.main_window.show_home)
        nav_layout.addWidget(back_button)
        
        # 弹性空间
        nav_layout.addStretch()
        
        # 标题
        title = QLabel(f"🎮 {language_manager.get_text('csgo_title')}")
        title.setObjectName("title_label")
        title.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(title)
        
        # 弹性空间
        nav_layout.addStretch()
        
        main_layout.addWidget(nav_frame)
        
        # 内容区域
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(25)
        
        # 添加服务器区域
        self.create_add_server_section(content_layout)
        
        # 查询服务器区域
        self.create_query_section(content_layout)
        
        # 服务器列表区域
        self.create_server_list_section(content_layout)
        
        # 显示默认服务器卡片
        self.load_default_servers()
        
        main_layout.addWidget(content_frame)
        self.setLayout(main_layout)

    def create_add_server_section(self, parent_layout):
        """Create add server section"""
        # 调试：打印当前用户信息
        print(f"当前用户: {self.main_window.current_user}")
        if self.main_window.current_user:
            print(f"用户名: {self.main_window.current_user.username}")
            print(f"是否管理员: {getattr(self.main_window.current_user, 'is_admin', False)}")
        
        # 检查管理员权限，非管理员不显示添加服务器区域
        if not self.main_window.current_user or not getattr(self.main_window.current_user, 'is_admin', False):
            print("权限检查失败：非管理员用户")
            return
            
        print("权限检查通过：显示添加服务器区域")
        add_group = QGroupBox(f"📝 {language_manager.get_text('add_new_server')}")
        add_layout = QGridLayout(add_group)
        add_layout.setSpacing(15)
        
        # 服务器名称
        add_layout.addWidget(QLabel(f"{language_manager.get_text('server_name')}:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(language_manager.get_text('server_name_placeholder'))
        add_layout.addWidget(self.name_input, 0, 1, 1, 2)
        
        # IP地址
        add_layout.addWidget(QLabel(f"{language_manager.get_text('ip_address')}:"), 1, 0)
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText(language_manager.get_text('ip_address_placeholder'))
        add_layout.addWidget(self.ip_input, 1, 1, 1, 2)
        
        # 端口
        add_layout.addWidget(QLabel(f"{language_manager.get_text('port')}:"), 2, 0)
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(27015)
        add_layout.addWidget(self.port_input, 2, 1)
        
        # 服务器类型
        add_layout.addWidget(QLabel(f"{language_manager.get_text('server_type')}:"), 2, 2)
        self.type_combo = QComboBox()
        self.type_combo.addItems([language_manager.get_text('competitive_mode'), language_manager.get_text('casual_mode'), language_manager.get_text('deathmatch'), language_manager.get_text('arms_race'), language_manager.get_text('demolition'), language_manager.get_text('custom')])
        add_layout.addWidget(self.type_combo, 2, 3)
        
        # 描述
        add_layout.addWidget(QLabel(f"{language_manager.get_text('description')}:"), 3, 0)
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText(language_manager.get_text('server_description_placeholder'))
        self.desc_input.setMaximumHeight(80)
        add_layout.addWidget(self.desc_input, 3, 1, 1, 3)
        
        # 添加按钮
        add_button = QPushButton(get_icon("add"), language_manager.get_text('add_server'))
        add_button.setObjectName("add_button")
        add_button.clicked.connect(self.add_server)
        add_layout.addWidget(add_button, 4, 1, 1, 2)
        
        parent_layout.addWidget(add_group)

    def load_default_servers(self):
        """加载并显示默认服务器卡片"""
        # 隐藏空状态提示
        if hasattr(self, 'empty_label'):
            self.empty_label.setVisible(False)
        
        # 为每个默认服务器创建卡片
        for server in self.default_servers:
            # 确保默认服务器标记为自定义服务器以显示按钮
            server_info = server.copy()
            server_info['is_custom'] = True  # 标记为自定义以显示操作按钮
            server_info['is_default'] = True  # 同时标记为默认服务器
            
            self.server_list.append(server_info)
            self.add_server_card(server_info)
        
        self.update_empty_state()
    
    def update_empty_state(self):
        """更新空状态显示"""
        if hasattr(self, 'empty_label'):
            # 如果有服务器卡片，隐藏空状态；否则显示空状态
            has_servers = len(self.server_list) > 0
            self.empty_label.setVisible(not has_servers)
    
    def create_add_server_section(self, parent_layout):
        """Create add server section"""
        # 检查管理员权限，非管理员不显示添加服务器区域
        if not self.main_window.current_user or not getattr(self.main_window.current_user, 'is_admin', False):
            return
            
        add_group = QGroupBox(f"📝 {language_manager.get_text('add_new_server')}")
        add_layout = QGridLayout(add_group)
        add_layout.setSpacing(15)
        
        # 服务器名称
        add_layout.addWidget(QLabel(f"{language_manager.get_text('server_name')}:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(language_manager.get_text('server_name_placeholder'))
        add_layout.addWidget(self.name_input, 0, 1, 1, 2)
        
        # IP地址
        add_layout.addWidget(QLabel(f"{language_manager.get_text('ip_address')}:"), 1, 0)
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText(language_manager.get_text('ip_address_placeholder'))
        add_layout.addWidget(self.ip_input, 1, 1, 1, 2)
        
        # 端口
        add_layout.addWidget(QLabel(f"{language_manager.get_text('port')}:"), 2, 0)
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(27015)
        add_layout.addWidget(self.port_input, 2, 1)
        
        # 服务器类型
        add_layout.addWidget(QLabel(f"{language_manager.get_text('server_type')}:"), 2, 2)
        self.type_combo = QComboBox()
        self.type_combo.addItems([language_manager.get_text('competitive_mode'), language_manager.get_text('casual_mode'), language_manager.get_text('deathmatch'), language_manager.get_text('arms_race'), language_manager.get_text('demolition'), language_manager.get_text('custom')])
        add_layout.addWidget(self.type_combo, 2, 3)
        
        # 描述
        add_layout.addWidget(QLabel(f"{language_manager.get_text('description')}:"), 3, 0)
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText(language_manager.get_text('server_description_placeholder'))
        self.desc_input.setMaximumHeight(80)
        add_layout.addWidget(self.desc_input, 3, 1, 1, 3)
        
        # 添加按钮
        add_button = QPushButton(get_icon("add"), language_manager.get_text('add_server'))
        add_button.setObjectName("add_button")
        add_button.clicked.connect(self.add_server)
        add_layout.addWidget(add_button, 4, 1, 1, 2)
        
        parent_layout.addWidget(add_group)
    
    def create_query_section(self, parent_layout):
        """Create query section"""
        query_group = QGroupBox(f"🔍 {language_manager.get_text('a2s_server_query')}")
        query_layout = QVBoxLayout(query_group)
        query_layout.setSpacing(15)
        
        # 查询说明
        info_label = QLabel(f"💡 {language_manager.get_text('a2s_query_info')}")
        info_label.setStyleSheet("color: #718096; font-style: italic; font-size: 13px;")
        query_layout.addWidget(info_label)
        
        # 地址输入
        address_layout = QHBoxLayout()
        address_label = QLabel(f"{language_manager.get_text('server_address')}:")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText(language_manager.get_text('server_address_placeholder'))
        self.address_input.returnPressed.connect(self.query_server)
        
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_input, 2)
        query_layout.addLayout(address_layout)
        
        # 按钮组
        button_layout = QHBoxLayout()
        
        self.query_button = QPushButton(get_icon("checkmark"), language_manager.get_text('query'))
        self.query_button.setObjectName("query_button")
        self.query_button.clicked.connect(self.query_server)
        
        self.clear_button = QPushButton(f"🗑️ {language_manager.get_text('clear_results')}")
        self.clear_button.setObjectName("clear_button")
        self.clear_button.clicked.connect(self.clear_results)
        
        button_layout.addWidget(self.query_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        query_layout.addLayout(button_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #667eea;
                border-radius: 10px;
                text-align: center;
                background: rgba(255,255,255,0.8);
                font-weight: bold;
                color: #2d3748;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
            }
        """)
        query_layout.addWidget(self.progress_bar)
        
        parent_layout.addWidget(query_group)
    
    def create_server_list_section(self, parent_layout):
        """Create server list section"""
        list_group = QGroupBox(f"📋 {language_manager.get_text('server_list')}")
        list_layout = QVBoxLayout(list_group)
        
        # 结果显示区域
        self.results_scroll = QScrollArea()
        self.results_scroll.setWidgetResizable(True)
        self.results_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.results_scroll.setMinimumHeight(300)
        
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        self.results_layout.setSpacing(15)
        
        # 空状态提示
        self.empty_label = QLabel(f"📭 {language_manager.get_text('no_server_info')}\n\n{language_manager.get_text('add_or_query_server_info')}")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("""
            QLabel {
                color: #a0aec0;
                font-size: 16px;
                font-style: italic;
                padding: 50px;
                border: 2px dashed #e2e8f0;
                border-radius: 15px;
                background: rgba(255,255,255,0.5);
            }
        """)
        self.results_layout.addWidget(self.empty_label)
        
        self.results_scroll.setWidget(self.results_widget)
        list_layout.addWidget(self.results_scroll)
        
        parent_layout.addWidget(list_group)
    
    def add_server(self):
        """Add server to list"""
        # 检查管理员权限
        if not self.main_window.current_user or not getattr(self.main_window.current_user, 'is_admin', False):
            QMessageBox.warning(self, language_manager.get_text('insufficient_permission'), language_manager.get_text('only_admin_can_add_server'))
            return
        
        name = self.name_input.text().strip()
        ip = self.ip_input.text().strip()
        port = self.port_input.value()
        server_type = self.type_combo.currentText()
        description = self.desc_input.toPlainText().strip()
        
        if not name or not ip:
            QMessageBox.warning(self, language_manager.get_text('warning'), language_manager.get_text('please_fill_server_name_ip'))
            return
        
        # 创建服务器信息
        server_info = {
            'name': name,
            'ip': ip,
            'port': port,
            'type': server_type,
            'description': description,
            'status': '未查询',
            'is_custom': True
        }
        
        self.server_list.append(server_info)
        self.add_server_card(server_info)
        
        # 清空输入框
        self.name_input.clear()
        self.ip_input.clear()
        self.port_input.setValue(27015)
        self.desc_input.clear()
        
        # 隐藏空状态提示
        self.empty_label.setVisible(False)
        
        QMessageBox.information(self, language_manager.get_text('success'), f"{language_manager.get_text('server_added_to_list').format(name=name)}")
    
    def add_server_card(self, server_info):
        """Add server card"""
        card_frame = QFrame()
        card_frame.setObjectName("server_card")
        card_layout = QVBoxLayout(card_frame)
        
        # 头部信息
        header_layout = QHBoxLayout()
        
        # 服务器名称和状态
        name_status_layout = QVBoxLayout()
        
        # 根据是否为默认服务器显示不同图标
        if server_info.get('is_default'):
            name_label = QLabel(f"🏆 {server_info['name']} ({language_manager.get_text('official')})")
        elif server_info.get('is_custom'):
            name_label = QLabel(f"🏷️ {server_info['name']}")
        else:
            name_label = QLabel(f"🖥️ {server_info['name']}")
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2d3748;")
        name_status_layout.addWidget(name_label)
        
        if server_info.get('is_custom'):
            status_label = QLabel(f"📍 {language_manager.get_text('type')}: {server_info['type']} | {language_manager.get_text('status')}: {server_info['status']}")
        else:
            status_label = QLabel(f"📊 {language_manager.get_text('status')}: {language_manager.get_text('online')} | {language_manager.get_text('players')}: {server_info.get('players', 0)}/{server_info.get('max_players', 0)}")
        status_label.setStyleSheet("color: #718096; font-size: 14px;")
        name_status_layout.addWidget(status_label)
        
        header_layout.addLayout(name_status_layout)
        header_layout.addStretch()
        
        # 操作按钮
        if server_info.get('is_custom'):
            query_btn = QPushButton(f"🔍 {language_manager.get_text('query')}")
            query_btn.clicked.connect(lambda: self.query_custom_server(server_info))
            header_layout.addWidget(query_btn)
            
            # 加入服务器按钮
            join_btn = QPushButton(f"🎮 {language_manager.get_text('join_server')}")
            join_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #28a745, stop:1 #20c997);
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #218838, stop:1 #17a2b8);
                }
            """)
            join_btn.clicked.connect(lambda: self.join_server(server_info))
            header_layout.addWidget(join_btn)
            
            # 只有非默认服务器才显示删除按钮
            if not server_info.get('is_default', False):
                remove_btn = QPushButton(f"🗑️ {language_manager.get_text('delete')}")
                remove_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #ff6b6b, stop:1 #ffa8a8);
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #ff5252, stop:1 #ff9999);
                    }
                """)
                remove_btn.clicked.connect(lambda: self.remove_server(card_frame, server_info))
                header_layout.addWidget(remove_btn)
        else:
            # 查询结果的服务器也添加加入按钮
            join_btn = QPushButton(f"🎮 {language_manager.get_text('join_server')}")
            join_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #28a745, stop:1 #20c997);
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #218838, stop:1 #17a2b8);
                }
            """)
            join_btn.clicked.connect(lambda: self.join_server(server_info))
            header_layout.addWidget(join_btn)
        
        card_layout.addLayout(header_layout)
        
        # 详细信息
        info_layout = QHBoxLayout()
        
        # 左侧信息
        left_info = QVBoxLayout()
        if server_info.get('is_custom'):
            left_info.addWidget(QLabel(f"🌐 {language_manager.get_text('address')}: {server_info['ip']}:{server_info['port']}"))
            if server_info.get('description'):
                desc_label = QLabel(f"📝 {language_manager.get_text('description')}: {server_info['description']}")
                desc_label.setWordWrap(True)
                left_info.addWidget(desc_label)
        else:
            left_info.addWidget(QLabel(f"🗺️ {language_manager.get_text('map')}: {server_info.get('map', 'N/A')}"))
            left_info.addWidget(QLabel(f"🌐 {language_manager.get_text('address')}: {server_info['ip']}:{server_info['port']}"))
        
        # 右侧信息
        right_info = QVBoxLayout()
        if not server_info.get('is_custom'):
            right_info.addWidget(QLabel(f"📡 {language_manager.get_text('ping')}: {server_info.get('ping', 'N/A')}ms"))
            right_info.addWidget(QLabel(f"⏰ {language_manager.get_text('query_time')}: {server_info.get('query_time', 'N/A')}"))
        
        info_layout.addLayout(left_info)
        if not server_info.get('is_custom'):
            info_layout.addLayout(right_info)
        
        card_layout.addLayout(info_layout)
        
        # 添加到结果区域
        self.results_layout.addWidget(card_frame)
    
    def query_custom_server(self, server_info):
        """Query custom server"""
        address_str = f"{server_info['ip']}:{server_info['port']}"
        self.address_input.setText(address_str)
        self.query_server()
    
    def join_server(self, server_info):
        """Join server through Steam"""
        try:
            import subprocess
            import webbrowser
            
            # 获取服务器IP和端口
            server_ip = server_info.get('ip', '')
            server_port = server_info.get('port', 27015)
            
            if not server_ip:
                QMessageBox.warning(self, language_manager.get_text('error'), language_manager.get_text('invalid_server_ip'))
                return
            
            # 构建Steam连接URL
            steam_url = f"steam://connect/{server_ip}:{server_port}"
            
            # 确认对话框
            reply = QMessageBox.question(self, language_manager.get_text('join_server'),
                                       f"{language_manager.get_text('steam_connect_confirm')}:\n{server_info.get('name', language_manager.get_text('unknown_server'))}\n{server_ip}:{server_port}\n\n{language_manager.get_text('confirm_continue')}",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # 尝试打开Steam URL
                try:
                    webbrowser.open(steam_url)
                    QMessageBox.information(self, language_manager.get_text('success'), language_manager.get_text('steam_connect_sent'))
                except Exception as e:
                    # 如果webbrowser失败，尝试使用subprocess
                    try:
                        subprocess.run(['start', steam_url], shell=True, check=True)
                        QMessageBox.information(self, language_manager.get_text('success'), language_manager.get_text('steam_connect_sent'))
                    except Exception as e2:
                        QMessageBox.warning(self, language_manager.get_text('error'), f"{language_manager.get_text('steam_connect_failed')}:\n{str(e2)}")
                        
        except Exception as e:
            QMessageBox.critical(self, language_manager.get_text('error'), f"{language_manager.get_text('join_server_error')}:\n{str(e)}")
    
    def remove_server(self, card_frame, server_info):
        """Remove server"""
        # 检查是否为默认服务器
        if server_info.get('is_default', False):
            QMessageBox.warning(self, language_manager.get_text('cannot_delete'), language_manager.get_text('admin_only_delete'))
            return
            
        reply = QMessageBox.question(self, language_manager.get_text('confirm_delete'), 
                                    f"{language_manager.get_text('confirm_delete_server')} '{server_info['name']}' ?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.server_list.remove(server_info)
            card_frame.deleteLater()
            self.update_empty_state()
    
    def query_server(self):
        """Query server"""
        address_str = self.address_input.text().strip()
        if not address_str:
            QMessageBox.warning(self, language_manager.get_text('warning'), language_manager.get_text('enter_server_address'))
            return
        
        # 解析地址
        address = CSGOServer.parse_address(address_str)
        if not address:
            QMessageBox.warning(self, language_manager.get_text('warning'), language_manager.get_text('invalid_address_format'))
            return
        
        # 开始查询
        self.query_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 无限进度条
        
        # 创建查询线程
        self.query_thread = ServerQueryThread(address)
        self.query_thread.result_ready.connect(self.on_query_success)
        self.query_thread.error_occurred.connect(self.on_query_error)
        self.query_thread.finished.connect(self.on_query_finished)
        self.query_thread.start()
    
    def on_query_success(self, result):
        """Query success callback"""
        # 将中文键名映射为英文键名，以匹配add_server_card的期望格式
        server_info = {
            'name': result.get('服务器名称', language_manager.get_text('unknown_server')),
             'map': result.get('地图', 'Unknown'),
            'players': result.get('玩家数量', 0),
            'max_players': result.get('最大玩家数', 0),
            'ping': result.get('延迟', 0),
            'ip': result.get('IP地址', ''),
            'port': result.get('端口', 27015),
            'game': result.get('游戏', ''),
            'version': result.get('版本', ''),
            'protocol': result.get('协议', ''),
            'player_list': result.get('玩家列表', [])
        }
        
        from datetime import datetime
        server_info['query_time'] = datetime.now().strftime("%H:%M:%S")
        server_info['is_custom'] = False
        
        self.add_server_card(server_info)
        self.empty_label.setVisible(False)
        
        QMessageBox.information(self, language_manager.get_text('query_success'), language_manager.get_text('server_query_complete'))
    
    def on_query_error(self, error_msg):
        """Query error callback"""
        QMessageBox.warning(self, language_manager.get_text('query_failed'), error_msg)
    
    def on_query_finished(self):
        """Query finished callback"""
        self.query_button.setEnabled(True)
        self.progress_bar.setVisible(False)
    
    def clear_results(self):
        """Clear query results"""
        reply = QMessageBox.question(self, language_manager.get_text('confirm_clear'), 
                                    language_manager.get_text('confirm_clear_results'),
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 清空服务器列表
            self.server_list.clear()
            
            # 移除所有卡片
            while self.results_layout.count() > 1:
                child = self.results_layout.takeAt(1)
                if child.widget():
                    child.widget().deleteLater()
            
            # 显示空状态
            self.empty_label.setVisible(True)
            
            QMessageBox.information(self, language_manager.get_text('clear_complete'), language_manager.get_text('results_cleared'))
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QMessageBox, QTableWidget,
                             QTableWidgetItem, QGroupBox, QComboBox, QProgressDialog, QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from database.db_operations import (get_user_by_id, update_user_points, 
                                   get_user_transactions, bind_steam_account,
                                   get_steam_binding)
from utils.payment import PaymentConfig
from utils.language_manager import language_manager
import requests

class UserProfileView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    # 在init_ui方法开始处添加整体样式
    def init_ui(self):
        """初始化个人中心UI"""
        # 设置整体背景和窗口属性
        self.setStyleSheet("""
            QWidget {
                background: #f8f9fa;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        # 创建滚动区域以防止内容被压缩
        from PyQt5.QtWidgets import QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #667eea;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #5a6fd8;
            }
        """)
        
        # 创建主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部导航栏
        nav_frame = QFrame()
        nav_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                padding: 10px;
                border: 1px solid #e0e0e0;
            }
        """)
        nav_layout = QHBoxLayout(nav_frame)
        
        # 返回商城按钮
        back_button = QPushButton("🏠 返回商城")
        back_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6fd8, stop:1 #6a4c93);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4c63d2, stop:1 #5d4084);
            }
        """)
        back_button.clicked.connect(self.main_window.show_home)
        nav_layout.addWidget(back_button)
        nav_layout.addStretch()
        
        # 添加个人中心标题
        self.title_label = QLabel(language_manager.get_text('profile_center'))
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                padding: 0px;
            }
        """)
        nav_layout.addWidget(self.title_label)
        nav_layout.addStretch()
        
        main_layout.addWidget(nav_frame)
        
        # 用户信息区域 - 重新设计
        info_frame = QFrame()
        info_frame.setObjectName("info_frame")
        info_frame.setStyleSheet("""
            QFrame#info_frame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 20px;
                padding: 30px;
                margin: 5px;
                min-height: 200px;
            }
        """)
        
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(15)
        
        # 用户信息标题
        self.info_title = QLabel(language_manager.get_text('user_info'))
        self.info_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 0px 0px 15px 0px;
                border-bottom: 2px solid rgba(255, 255, 255, 0.3);
                margin-bottom: 15px;
            }
        """)
        info_layout.addWidget(self.info_title)
        
        # 创建用户信息网格布局
        info_grid = QGridLayout()
        info_grid.setSpacing(12)
        
        # 创建信息标签
        self.username_label = QLabel()
        self.user_type_label = QLabel()
        self.display_name_label = QLabel()
        self.email_label = QLabel()
        self.points_label = QLabel()
        self.steam_status_label = QLabel()
        
        # 设置标签样式 - 确保文字不被压缩
        info_labels = [self.username_label, self.user_type_label, self.display_name_label, 
                      self.email_label, self.points_label, self.steam_status_label]
        
        for i, label in enumerate(info_labels):
            label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 16px;
                    font-weight: 600;
                    padding: 15px 20px;
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
                    min-height: 20px;
                    qproperty-wordWrap: true;
                }
            """)
            label.setWordWrap(True)  # 允许文字换行
            label.setMinimumHeight(50)  # 设置最小高度
            
            # 使用网格布局，每行两列
            row = i // 2
            col = i % 2
            info_grid.addWidget(label, row, col)
        
        info_layout.addLayout(info_grid)
        main_layout.addWidget(info_frame)
        
        # Steam绑定区域
        steam_frame = QFrame()
        steam_frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                padding: 25px;
                margin: 5px;
            }
        """)
        
        steam_layout = QVBoxLayout(steam_frame)
        steam_layout.setSpacing(15)
        
        # Steam绑定标题
        self.steam_title = QLabel(language_manager.get_text('steam_binding'))
        self.steam_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                padding: 10px 0px;
                border-bottom: 2px solid #667eea;
                margin-bottom: 15px;
            }
        """)
        steam_layout.addWidget(self.steam_title)
        
        # Steam输入区域
        steam_input_layout = QHBoxLayout()
        
        self.steam_id_input = QLineEdit()
        self.steam_id_input.setPlaceholderText(language_manager.get_text('enter_steam_id'))
        self.steam_id_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: #fafafa;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background: white;
            }
        """)
        steam_input_layout.addWidget(self.steam_id_input)
        
        self.bind_button = QPushButton(language_manager.get_text('bind_steam'))
        self.bind_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #20c997);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #218838, stop:1 #1ea085);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e7e34, stop:1 #198754);
            }
        """)
        self.bind_button.clicked.connect(self.handle_steam_bind)
        steam_input_layout.addWidget(self.bind_button)
        
        steam_layout.addLayout(steam_input_layout)
        main_layout.addWidget(steam_frame)
        
        # 积分充值区域 - 美化样式
        recharge_frame = QFrame()
        recharge_frame.setObjectName("recharge_frame")
        recharge_frame.setStyleSheet("""
            QFrame#recharge_frame {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                padding: 25px;
                margin: 10px;
            }
        """)
        
        recharge_layout = QVBoxLayout(recharge_frame)
        recharge_layout.setSpacing(15)
        
        # 充值标题
        self.recharge_title = QLabel(language_manager.get_text('points_recharge'))
        self.recharge_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #333;
                padding: 15px 0px;
                border-bottom: 3px solid #667eea;
                margin-bottom: 20px;
                text-align: center;
            }
        """)
        recharge_layout.addWidget(self.recharge_title)
        
        # 兑换比例显示（根据用户类型）
        user_type_for_rate = 'default'
        if self.main_window.current_user:
            if hasattr(self.main_window.current_user, 'user_type'):
                if self.main_window.current_user.user_type.value == 'vip':
                    user_type_for_rate = 'vip'
                elif self.main_window.current_user.user_type.value == 'admin':
                    user_type_for_rate = 'vip'  # 管理员享受VIP待遇
        
        exchange_rate = PaymentConfig.get_exchange_rate(user_type_for_rate)
        self.rate_label = QLabel(language_manager.get_text('exchange_rate').format(rate=exchange_rate))
        self.rate_label.setStyleSheet("""
            QLabel {
                color: #667eea;
                font-size: 15px;
                font-weight: 600;
                background: #f0f4ff;
                padding: 15px;
                border-radius: 10px;
                border-left: 5px solid #667eea;
                border: 1px solid #e0e8ff;
            }
        """)
        recharge_layout.addWidget(self.rate_label)
        
        # 充值金额输入
        amount_layout = QHBoxLayout()
        self.amount_label = QLabel(language_manager.get_text('recharge_amount'))
        self.amount_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: 600;
                color: #333;
                min-width: 90px;
                padding: 5px 0px;
            }
        """)
        amount_layout.addWidget(self.amount_label)
        
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText(language_manager.get_text('enter_amount'))
        self.amount_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background: #fafafa;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background: white;
            }
        """)
        self.amount_input.textChanged.connect(self.update_points_preview)
        amount_layout.addWidget(self.amount_input)
        recharge_layout.addLayout(amount_layout)
        
        # 积分预览
        self.points_preview = QLabel(language_manager.get_text('points_preview').format(points=0))
        self.points_preview.setStyleSheet("""
            QLabel {
                color: #28a745;
                font-weight: bold;
                font-size: 17px;
                background: #f8fff9;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #28a745;
                text-align: center;
            }
        """)
        recharge_layout.addWidget(self.points_preview)
        
        # 支付方式选择
        payment_layout = QHBoxLayout()
        self.payment_label = QLabel(language_manager.get_text('payment_method'))
        self.payment_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: 600;
                color: #333;
                min-width: 90px;
                padding: 5px 0px;
            }
        """)
        payment_layout.addWidget(self.payment_label)
        
        self.payment_method = QComboBox()
        self.payment_method.setStyleSheet("""
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                background: white;
                min-height: 20px;
            }
            QComboBox:hover {
                border: 2px solid #667eea;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }
        """)
        payment_methods = PaymentConfig.get_available_payment_methods()
        for method_id, method_info in payment_methods.items():
            self.payment_method.addItem(method_info['name'], method_id)
        payment_layout.addWidget(self.payment_method)
        recharge_layout.addLayout(payment_layout)
        
        # 充值按钮
        self.recharge_btn = QPushButton(language_manager.get_text('recharge_now'))
        self.recharge_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6fd8, stop:1 #6a4c93);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4c63d2, stop:1 #5d4084);
            }
        """)
        self.recharge_btn.clicked.connect(self.handle_recharge)
        recharge_layout.addWidget(self.recharge_btn)
        
        main_layout.addWidget(recharge_frame)
        
        # 积分交易记录 - 美化样式
        transactions_frame = QFrame()
        transactions_frame.setObjectName("transactions_frame")
        transactions_frame.setStyleSheet("""
            QFrame#transactions_frame {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                padding: 25px;
                margin: 5px;
                min-height: 300px;
            }
        """)
        
        transactions_layout = QVBoxLayout(transactions_frame)
        transactions_layout.setSpacing(15)
        
        # 交易记录标题
        self.transactions_title = QLabel(language_manager.get_text('transaction_history'))
        self.transactions_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                padding: 10px 0px;
                border-bottom: 2px solid #667eea;
                margin-bottom: 15px;
            }
        """)
        transactions_layout.addWidget(self.transactions_title)
        
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(4)
        self.transactions_table.setHorizontalHeaderLabels([
            language_manager.get_text('time'),
            language_manager.get_text('type'),
            language_manager.get_text('amount'),
            language_manager.get_text('description')
        ])
        self.transactions_table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #f0f0f0;
                font-size: 13px;
                min-height: 200px;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f0f0f0;
                font-size: 13px;
                min-height: 25px;
            }
            QTableWidget::item:selected {
                background: #f0f4ff;
                color: #333;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 12px 8px;
                border: none;
                font-weight: bold;
                font-size: 14px;
                min-height: 30px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 8px;
            }
        """)
        
        # 设置表格属性
        self.transactions_table.setAlternatingRowColors(True)
        self.transactions_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.transactions_table.horizontalHeader().setStretchLastSection(True)
        self.transactions_table.verticalHeader().setVisible(False)
        self.transactions_table.setMinimumHeight(250)
        
        # 设置列宽
        header = self.transactions_table.horizontalHeader()
        header.resizeSection(0, 150)  # 时间列
        header.resizeSection(1, 100)  # 类型列
        header.resizeSection(2, 100)  # 金额列
        # 描述列自动拉伸
        
        transactions_layout.addWidget(self.transactions_table)
        main_layout.addWidget(transactions_frame)
        
        # 设置滚动区域
        scroll_area.setWidget(main_widget)
        
        # 设置主布局
        main_container_layout = QVBoxLayout()
        main_container_layout.setContentsMargins(0, 0, 0, 0)
        main_container_layout.addWidget(scroll_area)
        self.setLayout(main_container_layout)
        
        # 加载用户数据
        self.load_user_data()
    
    def load_user_data(self):
        """加载用户数据"""
        if not self.main_window.current_user:
            return
        user = get_user_by_id(self.main_window.current_user.id)
        if user:
            self.username_label.setText(language_manager.get_text('username_label').format(username=user.username))
            
            # 显示用户类型和显示名称
            if hasattr(user, 'user_type') and user.user_type:
                user_type_display = user.get_type_display() if hasattr(user, 'get_type_display') else str(user.user_type)
                self.user_type_label.setText(language_manager.get_text('user_type_label').format(type=user_type_display))
                
                # 如果没有显示名称，自动生成一个
                if not user.display_name:
                    user.generate_display_name()
                    # 这里需要更新数据库，但为了简化，我们只在界面显示
                
                display_name = user.display_name if user.display_name else f"{user_type_display} - {user.username}"
                self.display_name_label.setText(language_manager.get_text('display_name_label').format(name=display_name))
            else:
                self.user_type_label.setText(language_manager.get_text('user_type_label').format(type=language_manager.get_text('normal_user')))
                self.display_name_label.setText(language_manager.get_text('display_name_label').format(name=f"{language_manager.get_text('normal_user')} - {user.username}"))
            
            self.email_label.setText(language_manager.get_text('email_label').format(email=user.email))
            self.points_label.setText(language_manager.get_text('points_balance').format(points=user.points))
            
            # 检查Steam绑定状态
            steam_binding = get_steam_binding(user.id)
            if steam_binding:
                self.steam_status_label.setText(language_manager.get_text('steam_account').format(name=steam_binding.steam_name))
            else:
                self.steam_status_label.setText(language_manager.get_text('steam_not_bound'))
            
            # 加载交易记录
            self.load_transactions()
    
    def load_transactions(self):
        """加载积分交易记录"""
        if not self.main_window.current_user:
            return
        transactions = get_user_transactions(self.main_window.current_user.id)
        self.transactions_table.setRowCount(len(transactions))
        
        for row, trans in enumerate(transactions):
            # 时间
            time_item = QTableWidgetItem(str(trans.created_at))
            self.transactions_table.setItem(row, 0, time_item)
            
            # 类型
            type_item = QTableWidgetItem(trans.type)
            self.transactions_table.setItem(row, 1, type_item)
            
            # 金额
            amount_item = QTableWidgetItem(str(trans.amount))
            self.transactions_table.setItem(row, 2, amount_item)
            
            # 描述
            desc_item = QTableWidgetItem(trans.description)
            self.transactions_table.setItem(row, 3, desc_item)
    
    def handle_steam_bind(self):
        """处理Steam账号绑定"""
        if not self.main_window.current_user:
            QMessageBox.warning(self, language_manager.get_text('error'), language_manager.get_text('please_login_first'))
            return
        steam_id = self.steam_id_input.text()
        if not steam_id:
            QMessageBox.warning(self, language_manager.get_text('error'), language_manager.get_text('please_enter_steam_id'))
            return
        
        try:
            # 调用Steam API获取用户信息
            # TODO: 实现Steam API调用
            steam_name = language_manager.get_text('test_user')  # 临时测试数据
            
            # 绑定Steam账号
            bind_steam_account(self.main_window.current_user.id, steam_id, steam_name)
            QMessageBox.information(self, language_manager.get_text('success'), language_manager.get_text('steam_bind_success'))
            self.load_user_data()
        except Exception as e:
            QMessageBox.warning(self, language_manager.get_text('error'), language_manager.get_text('bind_failed').format(error=str(e)))
    
    def update_points_preview(self):
        """更新积分预览"""
        try:
            amount = float(self.amount_input.text()) if self.amount_input.text() else 0
            if amount > 0:
                # 根据用户类型获取兑换比例
                user_type_for_rate = self._get_user_exchange_rate_type()
                exchange_rate = PaymentConfig.get_exchange_rate(user_type_for_rate)
                points = int(amount * exchange_rate)
                self.points_preview.setText(language_manager.get_text('points_preview').format(points=points))
            else:
                self.points_preview.setText(language_manager.get_text('points_preview').format(points=0))
        except ValueError:
            self.points_preview.setText(language_manager.get_text('points_preview').format(points=0))
    
    def _get_user_exchange_rate_type(self):
        """获取用户对应的兑换比例类型"""
        if not self.main_window.current_user:
            return 'default'
        
        if hasattr(self.main_window.current_user, 'user_type'):
            if self.main_window.current_user.user_type.value == 'vip':
                return 'vip'
            elif self.main_window.current_user.user_type.value == 'admin':
                return 'vip'  # 管理员享受VIP待遇
        
        return 'default'
    
    def handle_recharge(self):
        """处理积分充值"""
        if not self.main_window.current_user:
            QMessageBox.warning(self, language_manager.get_text('error'), language_manager.get_text('please_login_first'))
            return
        try:
            amount = float(self.amount_input.text())
            if amount <= 0:
                raise ValueError(language_manager.get_text('amount_must_positive'))
            if amount > 10000:
                raise ValueError(language_manager.get_text('amount_limit_exceeded'))
            
            # 获取兑换比例和支付方式
            # 根据用户类型获取兑换比例
            user_type_for_rate = self._get_user_exchange_rate_type()
            exchange_rate = PaymentConfig.get_exchange_rate(user_type_for_rate)
            points = int(amount * exchange_rate)
            payment_method = self.payment_method.currentData()
            
            # 确认充值信息
            confirm_msg = language_manager.get_text('recharge_confirm').format(
                amount=amount,
                points=points,
                method=self.payment_method.currentText()
            )
            
            reply = QMessageBox.question(self, language_manager.get_text('confirm_recharge'), confirm_msg, 
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # 调用支付接口
                payment_result = self.process_payment(amount, payment_method)
                
                if payment_result['success']:
                    # 支付验证成功后才增加积分
                    update_user_points(self.main_window.current_user.id, points)
                    QMessageBox.information(self, language_manager.get_text('recharge_success'), 
                                          language_manager.get_text('recharge_success_msg').format(
                                              payment_id=payment_result['payment_id'],
                                              points=points
                                          ))
                    self.amount_input.clear()
                    self.load_user_data()
                else:
                    QMessageBox.warning(self, language_manager.get_text('recharge_failed'), payment_result['message'])
                
        except ValueError as e:
            QMessageBox.warning(self, language_manager.get_text('input_error'), str(e))
        except Exception as e:
            QMessageBox.warning(self, language_manager.get_text('system_error'), language_manager.get_text('recharge_failed_msg').format(error=str(e)))
    
    def process_payment(self, amount, payment_method):
        """处理支付流程"""
        try:
            from utils.payment import PaymentAPI
            import time
            import uuid
            
            # 创建支付API实例
            payment_api = PaymentAPI()
            
            # 生成订单ID
            order_id = f"order_{int(time.time())}_{str(uuid.uuid4())[:8]}"
            
            # 显示支付处理对话框
            progress = QProgressDialog(language_manager.get_text('creating_payment_order'), language_manager.get_text('cancel'), 0, 100, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.setAutoClose(False)
            progress.setAutoReset(False)
            progress.show()
            progress.setValue(10)
            
            # 1. 创建支付订单
            payment_order = payment_api.create_payment(amount, order_id)
            
            if not payment_order:
                progress.close()
                return {'success': False, 'message': language_manager.get_text('create_order_failed'), 'payment_id': None}
            
            progress.setValue(30)
            progress.setLabelText(language_manager.get_text('order_created_complete_payment'))
            
            # 2. 获取支付二维码或支付链接
            payment_id = payment_order.get('payment_id')
            qr_code_url = payment_order.get('qr_code_url')
            
            if qr_code_url:
                # 显示二维码支付对话框
                qr_dialog = self.show_qr_payment_dialog(qr_code_url, amount, payment_method)
                if not qr_dialog:
                    progress.close()
                    return {'success': False, 'message': language_manager.get_text('user_cancelled_payment'), 'payment_id': payment_id}
            
            progress.setValue(50)
            progress.setLabelText(language_manager.get_text('waiting_payment_complete'))
            
            # 3. 轮询检查支付状态
            max_attempts = 60  # 最多等待5分钟
            attempt = 0
            
            while attempt < max_attempts:
                if progress.wasCanceled():
                    progress.close()
                    return {'success': False, 'message': language_manager.get_text('user_cancelled_payment'), 'payment_id': payment_id}
                
                # 检查支付状态
                payment_status = payment_api.check_payment(payment_id)
                
                if payment_status:
                    if payment_status.get('status') == 'success':
                        progress.setValue(100)
                        progress.setLabelText(language_manager.get_text('payment_success'))
                        time.sleep(1)
                        progress.close()
                        return {
                            'success': True,
                            'payment_id': payment_id,
                            'amount': amount,
                            'method': payment_method,
                            'message': language_manager.get_text('payment_success')
                        }
                    elif payment_status.get('status') == 'failed':
                        progress.close()
                        return {
                            'success': False,
                            'payment_id': payment_id,
                            'message': payment_status.get('message', language_manager.get_text('payment_failed'))
                        }
                
                # 等待5秒后再次检查
                time.sleep(5)
                attempt += 1
                progress.setValue(50 + (attempt * 40 // max_attempts))
            
            # 超时处理
            progress.close()
            return {
                'success': False,
                'payment_id': payment_id,
                'message': language_manager.get_text('payment_timeout')
            }
                
        except Exception as e:
            if 'progress' in locals():
                progress.close()
            print(f"{language_manager.get_text('payment_exception')}: {str(e)}")
            return {'success': False, 'message': f"{language_manager.get_text('payment_exception')}: {str(e)}", 'payment_id': None}
    
    def show_qr_payment_dialog(self, qr_code_url, amount, payment_method):
        """显示二维码支付对话框"""
        try:
            from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
            from PyQt5.QtCore import Qt
            from PyQt5.QtGui import QPixmap
            import requests
            import qrcode
            from io import BytesIO
            
            # 创建对话框
            dialog = QDialog(self)
            dialog.setWindowTitle(language_manager.get_text('scan_payment'))
            dialog.setFixedSize(400, 500)
            dialog.setWindowModality(Qt.ApplicationModal)
            
            layout = QVBoxLayout(dialog)
            
            # 支付信息
            info_label = QLabel(f"{language_manager.get_text('payment_amount')}：¥{amount}\n{language_manager.get_text('payment_method')}：{payment_method}\n{language_manager.get_text('scan_qr_to_pay')}")
            info_label.setAlignment(Qt.AlignCenter)
            info_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    padding: 20px;
                    background-color: #f5f5f5;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
            """)
            layout.addWidget(info_label)
            
            # 生成二维码
            qr_label = QLabel()
            qr_label.setAlignment(Qt.AlignCenter)
            
            try:
                # 生成二维码图片
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=8,
                    border=4,
                )
                qr.add_data(qr_code_url)
                qr.make(fit=True)
                
                # 创建二维码图片
                qr_img = qr.make_image(fill_color="black", back_color="white")
                
                # 转换为QPixmap
                buffer = BytesIO()
                qr_img.save(buffer, format='PNG')
                buffer.seek(0)
                
                pixmap = QPixmap()
                pixmap.loadFromData(buffer.getvalue())
                
                # 缩放二维码
                scaled_pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                qr_label.setPixmap(scaled_pixmap)
                
            except Exception as e:
                qr_label.setText(f"{language_manager.get_text('qr_generation_failed')}\n{str(e)}")
                qr_label.setStyleSheet("""
                    QLabel {
                        border: 2px dashed #ccc;
                        padding: 50px;
                        color: #666;
                    }
                """)
            
            layout.addWidget(qr_label)
            
            # 提示信息
            tip_label = QLabel(language_manager.get_text('payment_auto_detect'))
            tip_label.setAlignment(Qt.AlignCenter)
            tip_label.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-size: 12px;
                    padding: 10px;
                }
            """)
            layout.addWidget(tip_label)
            
            # 按钮
            button_layout = QHBoxLayout()
            
            cancel_btn = QPushButton(language_manager.get_text('cancel_payment'))
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
            """)
            cancel_btn.clicked.connect(dialog.reject)
            
            # 添加一个"已完成支付"按钮，让用户确认已经扫码支付
            confirm_btn = QPushButton(language_manager.get_text('payment_completed'))
            confirm_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            confirm_btn.clicked.connect(dialog.accept)
            
            button_layout.addWidget(cancel_btn)
            button_layout.addWidget(confirm_btn)
            layout.addLayout(button_layout)
            
            # 显示对话框
            result = dialog.exec_()
            return result == QDialog.Accepted
            
        except Exception as e:
            print(f"{language_manager.get_text('qr_dialog_exception')}: {str(e)}")
            return False

    def load_user_info(self):
        """加载用户信息（兼容主窗口调用）"""
        self.load_user_data()
    
    def update_language(self):
        """更新界面语言"""
        # 更新标题和标签文本
        self.title_label.setText(language_manager.get_text('personal_center'))
        
        # 更新用户信息区域
        self.info_title.setText(language_manager.get_text('user_info'))
        
        # 更新Steam绑定区域
        self.steam_title.setText(language_manager.get_text('steam_account_binding'))
        self.steam_id_input.setPlaceholderText(language_manager.get_text('enter_steam_id'))
        self.bind_button.setText(language_manager.get_text('bind_steam'))
        
        # 更新积分充值区域
        self.recharge_title.setText(language_manager.get_text('points_recharge'))
        self.amount_label.setText(language_manager.get_text('recharge_amount'))
        self.amount_input.setPlaceholderText(language_manager.get_text('enter_amount_yuan'))
        self.points_preview.setText(language_manager.get_text('will_get_points_0'))
        self.payment_label.setText(language_manager.get_text('payment_method'))
        self.recharge_btn.setText(language_manager.get_text('recharge_now'))
        
        # 更新交易记录区域
        self.transactions_title.setText(language_manager.get_text('transaction_records'))
        
        # 更新表格表头
        headers = [
            language_manager.get_text('time'),
            language_manager.get_text('type'),
            language_manager.get_text('amount'),
            language_manager.get_text('description')
        ]
        self.transactions_table.setHorizontalHeaderLabels(headers)
        
        # 重新加载用户数据以更新显示的文本
        self.load_user_data()
        
        # 更新兑换比例显示
        exchange_rate = self._get_user_exchange_rate_type()
        self.rate_label.setText(language_manager.get_text('current_exchange_rate').format(exchange_rate=exchange_rate))
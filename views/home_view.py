from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QFont
from database.db_operations import get_products, add_to_cart
from utils.language_manager import language_manager

class HomeView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 应用样式
        self.setStyleSheet(self._get_styles())
        
        # 创建导航栏
        nav_frame = self._create_nav_frame()
        main_layout.addWidget(nav_frame)
        
        # 创建内容区域
        content_frame = self._create_content_frame()
        main_layout.addWidget(content_frame)
        
        self.setLayout(main_layout)

    def _get_styles(self):
        return """
            QWidget {
                background: #f8f9fa;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            }
            QFrame#nav_frame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255,255,255,0.95), 
                    stop:1 rgba(255,255,255,0.85));
                border-radius: 15px;
                border: 2px solid rgba(255,255,255,0.4);
                margin: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            QFrame#content_frame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.9), 
                    stop:1 rgba(248,250,252,0.85));
                border-radius: 20px;
                margin: 15px;
                border: 2px solid rgba(255,255,255,0.3);
                box-shadow: 0 15px 35px rgba(0,0,0,0.08);
            }
            QFrame#product_card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.98), 
                    stop:1 rgba(248,250,252,0.95));
                border-radius: 15px;
                border: 2px solid rgba(255,255,255,0.5);
                margin: 10px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.06);
            }
            QFrame#product_card:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,1), 
                    stop:1 rgba(248,250,252,1));
                border: 2px solid rgba(102,126,234,0.4);
                box-shadow: 0 15px 40px rgba(102,126,234,0.15);
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
            QPushButton#add_cart_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
            }
            QPushButton#add_cart_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #45a049, stop:1 #3d8b40);
            }
            QLabel#title {
                font-size: 20px;
                font-weight: bold;
                color: #333;
                margin-bottom: 8px;
            }
            QLabel#desc {
                color: #666;
                font-size: 14px;
                margin-bottom: 10px;
            }
            QLabel#price {
                color: #e74c3c;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            QLabel#stock {
                color: #2196F3;
                font-size: 13px;
            }
            QLabel#user_info {
                font-size: 16px;
                color: #333;
                font-weight: 500;
                background: white;
                padding: 8px 15px;
                border-radius: 8px;
                border: 1px solid #ddd;
            }
            QLabel#app_title {
                font-size: 20px;
                font-weight: bold;
                color: #333;
                background: white;
                padding: 8px 15px;
                border-radius: 8px;
                border: 1px solid #ddd;
            }
            QPushButton#admin_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
            }
            QPushButton#admin_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6fd8, stop:1 #6a4190);
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
        """

    def _create_nav_frame(self):
        nav_frame = QFrame()
        nav_frame.setObjectName("nav_frame")
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setSpacing(15)
        nav_layout.setContentsMargins(20, 15, 20, 15)
        
        # 左侧logo和用户信息
        left_layout = self._create_left_nav()
        nav_layout.addLayout(left_layout)
        nav_layout.addStretch()
        
        # 右侧按钮组
        button_layout = self._create_nav_buttons()
        nav_layout.addLayout(button_layout)
        
        return nav_frame

    def _create_left_nav(self):
        left_layout = QHBoxLayout()
        left_layout.setSpacing(15)
        
        # Logo图标
        nav_icon = QLabel()
        nav_icon.setPixmap(QIcon("assets/icons/shop.ico").pixmap(32, 32))
        left_layout.addWidget(nav_icon)
        
        # 应用标题
        app_title = QLabel(language_manager.get_text('app_title'))
        app_title.setObjectName("app_title")
        left_layout.addWidget(app_title)
        
        left_layout.addStretch()
        
        # 用户信息
        self.user_info = QLabel()
        self.user_info.setObjectName("user_info")
        left_layout.addWidget(self.user_info)
        
        return left_layout

    def _create_nav_buttons(self):
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 购物车按钮
        self.cart_button = QPushButton(language_manager.get_text('cart'))
        self.cart_button.setIcon(QIcon("assets/icons/cart.ico"))
        self.cart_button.clicked.connect(self.main_window.show_cart)
        button_layout.addWidget(self.cart_button)
        
        # 个人中心按钮
        self.profile_button = QPushButton(language_manager.get_text('profile'))
        self.profile_button.setIcon(QIcon("assets/icons/user.ico"))
        self.profile_button.clicked.connect(self.main_window.show_profile)
        button_layout.addWidget(self.profile_button)
        
        # CSGO服务器查询按钮
        self.csgo_button = QPushButton(language_manager.get_text('csgo_server'))
        self.csgo_button.setIcon(QIcon("assets/icons/settings.ico"))
        self.csgo_button.clicked.connect(self.main_window.show_csgo_server)
        button_layout.addWidget(self.csgo_button)
        
        # 管理员按钮
        self.admin_button = QPushButton(language_manager.get_text('admin'))
        self.admin_button.setObjectName("admin_button")
        self.admin_button.setIcon(QIcon("assets/icons/admin.ico"))
        self.admin_button.setVisible(False)
        self.admin_button.clicked.connect(self.goto_admin)
        button_layout.addWidget(self.admin_button)
        
        # 退出登录按钮
        self.logout_button = QPushButton(language_manager.get_text('logout'))
        self.logout_button.setIcon(QIcon("assets/icons/logout.ico"))
        self.logout_button.clicked.connect(self.main_window.logout)
        button_layout.addWidget(self.logout_button)
        
        return button_layout

    def _create_content_frame(self):
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.products_widget = QWidget()
        self.products_layout = QVBoxLayout()
        self.products_widget.setLayout(self.products_layout)
        scroll.setWidget(self.products_widget)
        
        content_layout.addWidget(scroll)
        
        return content_frame

    def load_products(self):
        """加载商品并更新用户信息"""
        self._update_user_info()
        self._clear_products()
        self._load_product_list()

    def _update_user_info(self):
        """更新用户信息显示"""
        if self.main_window.current_user:
            username = self.main_window.current_user.username
            points = self.main_window.current_user.points
            self.user_info.setText(f"欢迎，{username} | 积分：{points}")
            
            # 显示管理员按钮
            if hasattr(self.main_window.current_user, 'is_admin') and self.main_window.current_user.is_admin:
                self.admin_button.setVisible(True)

    def _clear_products(self):
        """清空现有商品显示"""
        while self.products_layout.count():
            item = self.products_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _load_product_list(self):
        """加载商品列表"""
        products = get_products()
        if not products:
            self._show_empty_message()
            return
        
        for product in products:
            product_frame = self.create_product_frame(product)
            self.products_layout.addWidget(product_frame)
        
        self.products_layout.addStretch()

    def _show_empty_message(self):
        """显示无商品提示"""
        empty_label = QLabel("暂无商品")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setStyleSheet("font-size: 18px; color: #666; margin: 50px;")
        self.products_layout.addWidget(empty_label)

    def create_product_frame(self, product):
        """创建商品展示框架"""
        frame = QFrame()
        frame.setObjectName("product_card")
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 商品信息
        info_layout = self._create_product_info(product)
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # 操作按钮
        button_layout = self._create_product_button(product)
        layout.addLayout(button_layout)
        
        return frame

    def _create_product_info(self, product):
        """创建商品信息布局"""
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        
        # 商品名称
        name_label = QLabel(product.name)
        name_label.setObjectName("title")
        info_layout.addWidget(name_label)
        
        # 商品描述
        desc_label = QLabel(product.description)
        desc_label.setObjectName("desc")
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        # 价格
        price_label = QLabel(f"价格: {product.price} 积分")
        price_label.setObjectName("price")
        info_layout.addWidget(price_label)
        
        # 库存
        stock_label = QLabel(f"库存: {product.stock}")
        stock_label.setObjectName("stock")
        info_layout.addWidget(stock_label)
        
        return info_layout

    def _create_product_button(self, product):
        """创建商品操作按钮"""
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        
        add_button = QPushButton("加入购物车")
        add_button.setObjectName("add_cart_btn")
        add_button.setIcon(QIcon("assets/icons/cart.ico"))
        add_button.clicked.connect(lambda: self.add_to_cart(product))
        button_layout.addWidget(add_button)
        
        return button_layout

    def add_to_cart(self, product):
        """添加商品到购物车"""
        if not self._validate_user():
            return
        
        if not self._validate_stock(product):
            return
        
        self._perform_add_to_cart(product)

    def _validate_user(self):
        """验证用户登录状态"""
        if not self.main_window.current_user:
            QMessageBox.warning(self, "提示", "请先登录")
            return False
        return True

    def _validate_stock(self, product):
        """验证商品库存"""
        if product.stock <= 0:
            QMessageBox.warning(self, "提示", "商品库存不足")
            return False
        return True

    def _perform_add_to_cart(self, product):
        """执行添加到购物车操作"""
        try:
            success, message = add_to_cart(self.main_window.current_user.id, product.id, 1)
            if success:
                QMessageBox.information(self, "成功", "商品已加入购物车")
            else:
                QMessageBox.warning(self, "错误", message)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加入购物车失败: {str(e)}")

    def goto_admin(self):
        """跳转到管理员界面"""
        self.main_window.show_admin()
    
    def update_language(self):
        """更新语言"""
        # 更新按钮文本
        self.cart_button.setText(language_manager.get_text('cart'))
        self.profile_button.setText(language_manager.get_text('profile'))
        self.csgo_button.setText(language_manager.get_text('csgo_server'))
        self.admin_button.setText(language_manager.get_text('admin'))
        self.logout_button.setText(language_manager.get_text('logout'))
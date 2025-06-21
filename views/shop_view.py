from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QGridLayout, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from database.db_operations import get_products, get_user_by_id
from models.product import Product
from resources.icons import get_app_icon
from utils.language_manager import language_manager

class ProductCard(QFrame):
    def __init__(self, product: Product, parent=None):
        super().__init__(parent)
        self.product = product
        self.init_ui()
    
    def init_ui(self):
        """Initialize product card UI"""
        layout = QVBoxLayout()
        
        # Product image
        image_label = QLabel()
        if self.product.image_url:
            pixmap = QPixmap(self.product.image_url)
            image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            image_label.setText(language_manager.get_text('no_image'))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)
        
        # Product name
        name_label = QLabel(self.product.name)
        name_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(name_label)
        
        # Product price
        price_label = QLabel(f"{language_manager.get_text('points')}: {self.product.price}")
        layout.addWidget(price_label)
        
        # Stock information
        stock_label = QLabel(f"{language_manager.get_text('stock')}: {self.product.stock}")
        layout.addWidget(stock_label)
        
        # Buy button
        buy_button = QPushButton(language_manager.get_text('buy'))
        buy_button.clicked.connect(self.handle_buy)
        layout.addWidget(buy_button)
        
        self.setLayout(layout)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 5px;
                padding: 10px;
            }
        """)
    
    def handle_buy(self):
        """Handle buy operation"""
        # TODO: Implement buy logic
        pass

class ShopView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowIcon(get_app_icon())
        self.init_ui()
    
    # 在init_ui方法开始处添加整体样式
    def init_ui(self):
        """Initialize shop UI"""
        # Set overall background
        self.setStyleSheet("""
            QWidget {
                background: #f8f9fa;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Top navigation bar
        nav_layout = QHBoxLayout()
        
        # User information
        self.user_info = QLabel()
        nav_layout.addWidget(self.user_info)
        
        # Navigation buttons
        cart_button = QPushButton(language_manager.get_text('cart'))
        cart_button.clicked.connect(self.main_window.show_cart)
        nav_layout.addWidget(cart_button)
        
        profile_button = QPushButton(language_manager.get_text('profile'))
        profile_button.clicked.connect(self.main_window.show_profile)
        nav_layout.addWidget(profile_button)
        
        logout_button = QPushButton(language_manager.get_text('logout'))
        logout_button.clicked.connect(self.handle_logout)
        nav_layout.addWidget(logout_button)
        
        layout.addLayout(nav_layout)
        
        # 商品列表区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # 商品网格容器
        self.products_container = QWidget()
        self.products_grid = QGridLayout(self.products_container)
        scroll_area.setWidget(self.products_container)
        
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
        
        # 加载商品
        self.load_products()
    
    def load_products(self):
        """Load product list"""
        products = get_products()
        row = 0
        col = 0
        max_cols = 4  # Number of products per row
        
        for product in products:
            card = ProductCard(product)
            self.products_grid.addWidget(card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def handle_logout(self):
        """Handle logout"""
        self.main_window.show_login()
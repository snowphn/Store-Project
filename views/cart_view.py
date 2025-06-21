from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QMessageBox,
                             QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap
from database.db_operations import get_cart_items, update_cart_item, remove_from_cart, create_order
from resources.icons import get_app_icon, get_icon
from utils.language_manager import language_manager

class CartView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowIcon(get_app_icon())
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 应用增强样式
        # 在第22行左右，修改QWidget背景
        self.setStyleSheet("""
            QWidget {
                background: #f8f9fa;  # 改为浅灰白色
            }
            QFrame#header_frame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255,255,255,0.95), 
                    stop:1 rgba(255,255,255,0.85));
                border-radius: 15px;
                border: 2px solid rgba(255,255,255,0.4);
                margin: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            QFrame#cart_content {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255,255,255,0.9), 
                    stop:1 rgba(248,250,252,0.85));
                border-radius: 20px;
                margin: 15px;
                border: 2px solid rgba(255,255,255,0.3);
                box-shadow: 0 15px 35px rgba(0,0,0,0.08);
            }
            QFrame#cart_item {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255,255,255,0.98), 
                    stop:1 rgba(248,250,252,0.95));
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.6);
                margin: 8px;
                padding: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            }
            QFrame#header_frame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 0 0 20px 20px;
                border: none;
                padding: 20px;
            }
            QFrame#cart_item {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                margin: 10px;
                padding: 20px;
            }
            QFrame#cart_item:hover {
                background: rgba(255, 255, 255, 1.0);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            QFrame#total_frame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 2px solid #667eea;
                margin: 20px;
                padding: 25px;
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
                transform: translateY(-1px);
            }
            QPushButton#checkout_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                font-size: 16px;
                padding: 15px 30px;
            }
            QPushButton#checkout_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #45a049, stop:1 #3d8b40);
            }
            QPushButton#remove_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
            }
            QPushButton#remove_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c0392b, stop:1 #a93226);
            }
            QSpinBox {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                min-width: 60px;
            }
            QSpinBox:focus {
                border-color: #667eea;
            }
            QLabel#title {
                font-size: 32px;
                font-weight: bold;
                color: #333;
            }
            QLabel#item_name {
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }
            QLabel#item_price {
                font-size: 16px;
                color: #e74c3c;
                font-weight: bold;
            }
            QLabel#total_label {
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        # 头部
        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        self.back_button = QPushButton(get_icon("back"), language_manager.get_text('back'))
        self.back_button.clicked.connect(self.main_window.show_home)
        header_layout.addWidget(self.back_button)
        
        header_layout.addStretch()
        
        self.title = QLabel(language_manager.get_text('cart_title'))
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.title)
        
        header_layout.addStretch()
        
        # 占位，保持标题居中
        placeholder = QLabel()
        placeholder.setFixedWidth(self.back_button.sizeHint().width())
        header_layout.addWidget(placeholder)
        
        main_layout.addWidget(header_frame)
        
        # 购物车内容区域
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.cart_widget = QWidget()
        self.cart_layout = QVBoxLayout()
        self.cart_widget.setLayout(self.cart_layout)
        scroll.setWidget(self.cart_widget)
        
        content_layout.addWidget(scroll)
        
        # 总计和结算区域
        self.total_frame = QFrame()
        self.total_frame.setObjectName("total_frame")
        total_layout = QHBoxLayout(self.total_frame)
        total_layout.setSpacing(20)
        
        self.total_label = QLabel(f"{language_manager.get_text('total')}: 0 {language_manager.get_text('points')}")
        self.total_label.setObjectName("total_label")
        total_layout.addWidget(self.total_label)
        
        total_layout.addStretch()
        
        self.checkout_button = QPushButton(get_icon("checkmark"), language_manager.get_text('checkout'))
        self.checkout_button.setObjectName("checkout_btn")
        self.checkout_button.clicked.connect(self.checkout)
        total_layout.addWidget(self.checkout_button)
        
        content_layout.addWidget(self.total_frame)
        main_layout.addWidget(content_frame)
        
        self.setLayout(main_layout)

    def load_cart_items(self):
        # 清空现有项目
        while self.cart_layout.count():
            item = self.cart_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.main_window.current_user:
            return
        
        cart_items = get_cart_items(self.main_window.current_user.id)
        
        if not cart_items:
            self.empty_label = QLabel(language_manager.get_text('empty_cart'))
            self.empty_label.setAlignment(Qt.AlignCenter)
            self.empty_label.setStyleSheet("font-size: 18px; color: white; margin: 50px;")
            self.cart_layout.addWidget(self.empty_label)
            self.total_frame.setVisible(False)
            return
        
        self.total_frame.setVisible(True)
        total_points = 0
        
        for item in cart_items:
            item_frame = self.create_cart_item_frame(item)
            self.cart_layout.addWidget(item_frame)
            total_points += item.product.price * item.quantity
        
        self.cart_layout.addStretch()
        self.total_label.setText(f"{language_manager.get_text('total')}: {total_points} {language_manager.get_text('points')}")

    def create_cart_item_frame(self, cart_item):
        frame = QFrame()
        frame.setObjectName("cart_item")
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # 商品信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        
        name_label = QLabel(cart_item.product.name)
        name_label.setObjectName("item_name")
        info_layout.addWidget(name_label)
        
        price_label = QLabel(f"{language_manager.get_text('unit_price')}: {cart_item.product.price} {language_manager.get_text('points')}")
        price_label.setObjectName("item_price")
        info_layout.addWidget(price_label)
        
        subtotal_label = QLabel(f"{language_manager.get_text('subtotal')}: {cart_item.product.price * cart_item.quantity} {language_manager.get_text('points')}")
        subtotal_label.setStyleSheet("font-size: 14px; color: #666;")
        info_layout.addWidget(subtotal_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # 数量控制
        quantity_layout = QVBoxLayout()
        quantity_layout.setAlignment(Qt.AlignCenter)
        
        quantity_label = QLabel(f"{language_manager.get_text('quantity')}:")
        quantity_label.setStyleSheet("font-size: 14px; color: #666;")
        quantity_layout.addWidget(quantity_label)
        
        quantity_spinbox = QSpinBox()
        quantity_spinbox.setRange(1, 99)
        quantity_spinbox.setValue(cart_item.quantity)
        quantity_spinbox.valueChanged.connect(
            lambda value: self.update_quantity(cart_item.id, value)
        )
        quantity_layout.addWidget(quantity_spinbox)
        
        layout.addLayout(quantity_layout)
        
        # Remove button
        remove_button = QPushButton(get_icon("delete"), language_manager.get_text('remove'))
        remove_button.setObjectName("remove_btn")
        remove_button.clicked.connect(lambda: self.remove_item(cart_item.id))
        layout.addWidget(remove_button)
        
        return frame

    def update_quantity(self, cart_item_id, quantity):
        try:
            success, message = update_cart_item(cart_item_id, quantity)
            if success:
                self.load_cart_items()  # Reload to update total
            else:
                QMessageBox.warning(self, language_manager.get_text('error'), message)
        except Exception as e:
            QMessageBox.warning(self, language_manager.get_text('error'), f"{language_manager.get_text('update_quantity_failed')}: {str(e)}")

    def remove_item(self, cart_item_id):
        reply = QMessageBox.question(
            self, language_manager.get_text('confirm_delete'), language_manager.get_text('confirm_remove_item'),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success, message = remove_from_cart(cart_item_id)
                if success:
                    self.load_cart_items()
                else:
                    QMessageBox.warning(self, language_manager.get_text('error'), message)
            except Exception as e:
                QMessageBox.warning(self, language_manager.get_text('error'), f"{language_manager.get_text('remove_item_failed')}: {str(e)}")

    def checkout(self):
        if not self.main_window.current_user:
            QMessageBox.warning(self, language_manager.get_text('info'), language_manager.get_text('please_login_first'))
            return
        
        cart_items = get_cart_items(self.main_window.current_user.id)
        if not cart_items:
            QMessageBox.warning(self, language_manager.get_text('info'), language_manager.get_text('cart_empty'))
            return
        
        total_points = sum(item.product.price * item.quantity for item in cart_items)
        
        if self.main_window.current_user.points < total_points:
            QMessageBox.warning(self, language_manager.get_text('insufficient_points'), f"{language_manager.get_text('insufficient_points_message')} {total_points} {language_manager.get_text('points')}")
            return
        
        reply = QMessageBox.question(
            self, language_manager.get_text('confirm_checkout'), f"{language_manager.get_text('confirm_spend')} {total_points} {language_manager.get_text('points')}{language_manager.get_text('buy_items')}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success, message = create_order(self.main_window.current_user.id)
                if success:
                    QMessageBox.information(self, language_manager.get_text('success'), language_manager.get_text('order_created_success'))
                    self.load_cart_items()
                    # Update user points display
                    self.main_window.current_user = get_user_by_username(self.main_window.current_user.username)
                else:
                    QMessageBox.warning(self, language_manager.get_text('error'), message)
            except Exception as e:
                QMessageBox.warning(self, language_manager.get_text('error'), f"{language_manager.get_text('create_order_failed')}: {str(e)}")
    
    def update_language(self):
        """Update language"""
        # Update button and label text
        self.back_button.setText(language_manager.get_text('back'))
        self.title.setText(language_manager.get_text('cart_title'))
        self.checkout_button.setText(language_manager.get_text('checkout'))
        
        # Reload cart items to update text
        self.load_cart_items()
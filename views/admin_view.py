from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QScrollArea, QFrame, QMessageBox,
                             QDialog, QLineEdit, QFormLayout, QSpinBox,
                             QDoubleSpinBox, QComboBox, QTabWidget, QGroupBox,
                             QCheckBox, QInputDialog, QTextEdit, QTableWidget,
                             QTableWidgetItem)
from PyQt5.QtCore import Qt
from database.db_operations import (get_all_users, get_all_products, get_all_orders,
                                   create_product, update_product, delete_product, reset_all_data,
                                   create_invite_code, get_invite_codes, delete_invite_code)
from models.user import User
import json
from database.db_init import SessionLocal
from controllers.user_controller import create_admin_user
from resources.icons import get_app_icon, get_icon
from utils.language_manager import language_manager
from PyQt5.QtGui import QIcon, QPixmap

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(get_app_icon())
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("添加商品")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # 商品名称
        name_layout = QHBoxLayout()
        name_label = QLabel("商品名称:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # 商品描述
        desc_layout = QHBoxLayout()
        desc_label = QLabel("商品描述:")
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        layout.addLayout(desc_layout)
        
        # 商品价格
        price_layout = QHBoxLayout()
        price_label = QLabel("商品价格:")
        self.price_input = QSpinBox()
        self.price_input.setRange(0, 1000000)
        price_layout.addWidget(price_label)
        price_layout.addWidget(self.price_input)
        layout.addLayout(price_layout)
        
        # 商品库存
        stock_layout = QHBoxLayout()
        stock_label = QLabel("商品库存:")
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 1000000)
        stock_layout.addWidget(stock_label)
        stock_layout.addWidget(self.stock_input)
        layout.addLayout(stock_layout)
        
        # 商品分类
        category_layout = QHBoxLayout()
        category_label = QLabel("商品分类:")
        self.category_input = QComboBox()
        self.category_input.addItems(["皮肤", "特效", "枪模", "浮游炮"])
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_input)
        layout.addLayout(category_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

class AdminView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowIcon(get_app_icon())
        self.session = SessionLocal()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        # 设置整体背景
        self.setStyleSheet("""
            QWidget {
                background: #f8f9fa;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 导航栏样式
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        
        back_button = QPushButton(get_icon("back"), language_manager.get_text('back_to_shop'))
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
        
        nav_layout.addStretch()
        
        add_product_button = QPushButton("添加商品")
        add_product_button.setStyleSheet("""
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
            }
        """)
        # 在导航栏布局中添加管理员按钮（在添加商品按钮后）
        add_product_button.clicked.connect(self.show_add_product_dialog)
        nav_layout.addWidget(add_product_button)
        
        # 添加管理员按钮
        add_admin_button = QPushButton(get_icon("admin"), language_manager.get_text('add_admin'))
        add_admin_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #9b59b6, stop:1 #8e44ad);
                color: white;
                border: none;
                padding: 10px 18px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8e44ad, stop:1 #7d3c98);
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(142, 68, 173, 0.3);
            }
            QPushButton:pressed {
                transform: translateY(0px);
            }
        """)
        add_admin_button.clicked.connect(self.create_admin)
        nav_layout.addWidget(add_admin_button)
        
        reset_button = QPushButton("重置所有数据")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        reset_button.clicked.connect(self.reset_all_data_action)
        nav_layout.addWidget(reset_button)
        
        layout.addLayout(nav_layout)
        
        # 标签页样式
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background: white;
            }
            QTabBar::tab {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
            }
            QTabBar::tab:hover {
                background: #e9ecef;
            }
        """)
        
        self.users_tab = QWidget()
        self.init_users_tab()
        self.tab_widget.addTab(self.users_tab, "用户管理")
        
        self.products_tab = QWidget()
        self.init_products_tab()
        self.tab_widget.addTab(self.products_tab, "商品管理")
        
        self.orders_tab = QWidget()
        self.init_orders_tab()
        self.tab_widget.addTab(self.orders_tab, "订单管理")
        
        # 邀请码管理
        invite_code_layout = QVBoxLayout()
        invite_code_title = QLabel("邀请码管理")
        invite_code_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #222; margin-bottom: 20px;")
        invite_code_title.setAlignment(Qt.AlignCenter)
        invite_code_layout.addWidget(invite_code_title)
        generate_button = QPushButton("生成邀请码")
        generate_button.clicked.connect(self.generate_invite_code)
        invite_code_layout.addWidget(generate_button)
        self.invite_code_table = QTableWidget()
        self.invite_code_table.setColumnCount(4)
        self.invite_code_table.setHorizontalHeaderLabels(["邀请码", "状态", "创建时间", "操作"])
        invite_code_layout.addWidget(self.invite_code_table)
        layout.addLayout(invite_code_layout)
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        self.load_invite_codes()

    def init_users_tab(self):
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.users_widget = QWidget()
        self.users_layout = QVBoxLayout()
        self.users_widget.setLayout(self.users_layout)
        scroll.setWidget(self.users_widget)
        layout.addWidget(scroll)
        layout.addStretch()
        if self.main_window.current_user and getattr(self.main_window.current_user, 'is_admin', False):
            add_admin_button = QPushButton("增加管理员账号")
            add_admin_button.setStyleSheet("background-color: #007bff; color: white; border-radius: 6px;")
            add_admin_button.clicked.connect(self.create_admin)
            layout.addWidget(add_admin_button)
        self.users_tab.setLayout(layout)

    def init_products_tab(self):
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.products_widget = QWidget()
        self.products_layout = QVBoxLayout()
        self.products_widget.setLayout(self.products_layout)
        scroll.setWidget(self.products_widget)
        layout.addWidget(scroll)
        self.products_tab.setLayout(layout)

    def init_orders_tab(self):
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.orders_widget = QWidget()
        self.orders_layout = QVBoxLayout()
        self.orders_widget.setLayout(self.orders_layout)
        scroll.setWidget(self.orders_widget)
        layout.addWidget(scroll)
        self.orders_tab.setLayout(layout)

    def load_data(self):
        self.load_users()
        self.load_products()
        self.load_orders()

    def load_users(self):
        self.session.close()
        from database.db_init import SessionLocal
        self.session = SessionLocal()
        while self.users_layout.count():
            item = self.users_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        users = get_all_users()
        if not users:
            empty_label = QLabel("暂无用户")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("font-size: 16px; color: #666;")
            self.users_layout.addWidget(empty_label)
            return
        for user in users:
            user_frame = self.create_user_frame(user)
            self.users_layout.addWidget(user_frame)
        self.users_layout.addStretch()

    def load_products(self):
        while self.products_layout.count():
            item = self.products_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        products = get_all_products()
        if not products:
            empty_label = QLabel("暂无商品")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("font-size: 16px; color: #666;")
            self.products_layout.addWidget(empty_label)
            return
        for product in products:
            product_frame = self.create_product_frame(product)
            self.products_layout.addWidget(product_frame)
        self.products_layout.addStretch()

    def load_orders(self):
        while self.orders_layout.count():
            item = self.orders_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        orders = get_all_orders()
        if not orders:
            empty_label = QLabel("暂无订单")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("font-size: 16px; color: #666;")
            self.orders_layout.addWidget(empty_label)
            return
        for order in orders:
            order_frame = self.create_order_frame(order)
            self.orders_layout.addWidget(order_frame)
        self.orders_layout.addStretch()

    def create_user_frame(self, user):
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin: 5px;
            }
            QFrame:hover {
                border-color: #007bff;
                box-shadow: 0 0 5px rgba(0,123,255,0.3);
            }
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        
        name_label = QLabel(f"用户名: {user.username}")
        name_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #212529;")
        info_layout.addWidget(name_label)
        
        # 显示用户类型和显示名称
        if hasattr(user, 'user_type') and user.user_type:
            user_type_display = user.get_type_display() if hasattr(user, 'get_type_display') else str(user.user_type)
            type_label = QLabel(f"类型: {user_type_display}")
            type_label.setStyleSheet("font-size: 13px; color: #007bff; font-weight: bold;")
            info_layout.addWidget(type_label)
            
            if user.display_name:
                display_name_label = QLabel(f"显示名称: {user.display_name}")
                display_name_label.setStyleSheet("font-size: 12px; color: #6c757d;")
                info_layout.addWidget(display_name_label)
        
        email_label = QLabel(f"邮箱: {user.email}")
        email_label.setStyleSheet("font-size: 14px; color: #6c757d;")
        info_layout.addWidget(email_label)
        
        points_label = QLabel(f"积分: {user.points}")
        points_label.setStyleSheet("font-size: 14px; color: #28a745; font-weight: bold;")
        info_layout.addWidget(points_label)
        
        # 显示使用的邀请码
        if hasattr(user, 'invite_code_used') and user.invite_code_used:
            invite_label = QLabel(f"邀请码: {user.invite_code_used}")
            invite_label.setStyleSheet("font-size: 12px; color: #ffc107;")
            info_layout.addWidget(invite_label)
        
        layout.addLayout(info_layout)
        
        button_layout = QVBoxLayout()
        button_layout.setSpacing(8)
        
        ban_button = QPushButton("解禁账号" if user.is_banned else "封禁账号")
        ban_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        ban_button.clicked.connect(lambda: self.ban_user_dialog(user))
        button_layout.addWidget(ban_button)
        
        modify_points_button = QPushButton("修改点数")
        modify_points_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        modify_points_button.clicked.connect(lambda: self.modify_user_points_dialog(user))
        button_layout.addWidget(modify_points_button)
        
        # 新增：删除用户按钮
        delete_user_button = QPushButton("删除用户")
        delete_user_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_user_button.clicked.connect(lambda: self.delete_user_dialog(user))
        button_layout.addWidget(delete_user_button)
        
        layout.addLayout(button_layout)
        frame.setLayout(layout)
        return frame

    def ban_user_dialog(self, user):
        action = "解禁" if user.is_banned else "封禁"
        reply = QMessageBox.question(
            self,
            f"确认{action}",
            f"确定要{action}用户 {user.username} 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                user.is_banned = not user.is_banned
                self.session.commit()
                self.session.expire_all()
                QMessageBox.information(self, "成功", f"用户 {user.username} 已{action}")
                self.load_users()
            except Exception as e:
                QMessageBox.warning(self, "错误", f"{action}用户失败: {str(e)}")

    def modify_user_points_dialog(self, user):
        db_user = self.session.query(User).filter_by(id=user.id).first()
        points, ok = QInputDialog.getInt(
            self,
            "修改商店点数",
            f"请输入新的商店点数（当前：{db_user.points}）:",
            int(db_user.points),
            0,
            1000000
        )
        if ok:
            try:
                db_user.points = points
                self.session.commit()
                self.session.expire_all()
                QMessageBox.information(self, "成功", f"用户 {db_user.username} 的商店点数已修改为 {points}")
                self.load_users()
            except Exception as e:
                QMessageBox.warning(self, "错误", f"修改点数失败: {str(e)}")

    def delete_user_dialog(self, user):
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除用户 {user.username} 吗？此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                db_user = self.session.query(User).filter_by(id=user.id).first()
                if db_user:
                    self.session.delete(db_user)
                    self.session.commit()
                    self.session.expire_all()
                    QMessageBox.information(self, "成功", f"用户 {user.username} 已被删除")
                    self.load_users()
                else:
                    QMessageBox.warning(self, "错误", "用户不存在")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"删除用户失败: {str(e)}")

    def create_product_frame(self, product):
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin: 5px;
            }
            QFrame:hover {
                border-color: #007bff;
                box-shadow: 0 0 5px rgba(0,123,255,0.3);
            }
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        
        name_label = QLabel(product.name)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #212529;")
        info_layout.addWidget(name_label)
        
        desc_label = QLabel(product.description)
        desc_label.setStyleSheet("font-size: 14px; color: #6c757d;")
        info_layout.addWidget(desc_label)
        
        price_label = QLabel(f"价格: {product.price} 积分")
        price_label.setStyleSheet("font-size: 14px; color: #28a745; font-weight: bold;")
        info_layout.addWidget(price_label)
        
        stock_label = QLabel(f"库存: {product.stock}")
        stock_label.setStyleSheet("font-size: 14px; color: #6c757d;")
        info_layout.addWidget(stock_label)
        
        layout.addLayout(info_layout)
        
        button_layout = QVBoxLayout()
        button_layout.setSpacing(8)
            
        edit_button = QPushButton("编辑")
        edit_button.clicked.connect(lambda: self.show_edit_product_dialog(product))
        button_layout.addWidget(edit_button)
            
        delete_button = QPushButton("删除")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_button.clicked.connect(lambda: self.delete_product(product.id))
        button_layout.addWidget(delete_button)
            
        layout.addLayout(button_layout)
        frame.setLayout(layout)
        return frame

    def create_order_frame(self, order):
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin: 5px;
            }
            QFrame:hover {
                border-color: #007bff;
                box-shadow: 0 0 5px rgba(0,123,255,0.3);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        order_id_label = QLabel(f"订单号: {order.id}")
        order_id_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #212529;")
        header_layout.addWidget(order_id_label)
        
        user_label = QLabel(f"用户: {order.user.username}")
        user_label.setStyleSheet("font-size: 14px; color: #6c757d;")
        header_layout.addWidget(user_label)
        
        date_label = QLabel(f"下单时间: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        date_label.setStyleSheet("font-size: 14px; color: #6c757d;")
        header_layout.addWidget(date_label)
        
        status_label = QLabel(f"状态: {order.status}")
        status_label.setStyleSheet("font-size: 14px; color: #28a745; font-weight: bold;")
        header_layout.addWidget(status_label)
        
        layout.addLayout(header_layout)
        
        for item in order.items:
            item_frame = QFrame()
            item_frame.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border-radius: 4px;
                    padding: 8px;
                }
            """)
            
            item_layout = QHBoxLayout()
            item_layout.setSpacing(10)
            
            name_label = QLabel(item["name"])
            name_label.setStyleSheet("font-size: 14px; color: #212529;")
            item_layout.addWidget(name_label)
            
            price_label = QLabel(f"单价: {item['price']} 积分")
            price_label.setStyleSheet("font-size: 14px; color: #6c757d;")
            item_layout.addWidget(price_label)
            
            quantity_label = QLabel(f"数量: {item['quantity']}")
            quantity_label.setStyleSheet("font-size: 14px; color: #6c757d;")
            item_layout.addWidget(quantity_label)
            
            subtotal_label = QLabel(f"小计: {item['price'] * item['quantity']} 积分")
            subtotal_label.setStyleSheet("font-size: 14px; color: #28a745; font-weight: bold;")
            item_layout.addWidget(subtotal_label)
            
            item_frame.setLayout(item_layout)
            layout.addWidget(item_frame)
        
        total_label = QLabel(f"总计: {order.total_points} 积分")
        total_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #28a745;")
        total_label.setAlignment(Qt.AlignRight)
        layout.addWidget(total_label)
        
        frame.setLayout(layout)
        return frame

    def show_add_product_dialog(self):
        dialog = AddProductDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                success, message = create_product(
                    name=dialog.name_input.text().strip(),
                    description=dialog.desc_input.toPlainText().strip(),
                    price=dialog.price_input.value(),
                    stock=dialog.stock_input.value(),
                    category=dialog.category_input.currentText()
                )
                if success:
                    QMessageBox.information(self, "成功", message)
                    self.load_products()
                else:
                    QMessageBox.warning(self, "错误", message)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"添加商品失败: {str(e)}")
    
    def show_edit_product_dialog(self, product):
        dialog = AddProductDialog(self)
        dialog.setWindowTitle("编辑商品")
        dialog.name_input.setText(product.name)
        dialog.desc_input.setText(product.description)
        dialog.price_input.setValue(product.price)
        dialog.stock_input.setValue(product.stock)
        dialog.category_input.setCurrentText(product.category)
        if dialog.exec_() == QDialog.Accepted:
            try:
                success, message = update_product(
                    product_id=product.id,
                    name=dialog.name_input.text().strip(),
                    description=dialog.desc_input.toPlainText().strip(),
                    price=dialog.price_input.value(),
                    stock=dialog.stock_input.value(),
                    category=dialog.category_input.currentText()
                )
                if success:
                    QMessageBox.information(self, "成功", message)
                    self.load_products()
                else:
                    QMessageBox.warning(self, "错误", message)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"更新商品失败: {str(e)}")

    def delete_product(self, product_id):
        reply = QMessageBox.question(
            self,
            "确认删除",
            "确定要删除这个商品吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                success, message = delete_product(product_id)
                if success:
                    QMessageBox.information(self, "成功", message)
                    self.load_products()
                else:
                    QMessageBox.warning(self, "错误", message)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"删除商品失败: {str(e)}")
    
    def reset_all_data_action(self):
        reply = QMessageBox.question(
            self,
            "确认重置",
            "此操作将清空所有用户、商品、订单等数据，且不可恢复，确定继续吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            db = SessionLocal()
            try:
                # 删除所有数据
                db.query(CartItem).delete()
                db.query(Order).delete()
                db.query(Product).delete()
                db.query(User).delete()
                db.commit()
                
                # 重新创建管理员账号
                self.create_admin()
                
                QMessageBox.information(self, "成功", "所有数据已重置")
                self.load_data()
            except Exception as e:
                db.rollback()
                QMessageBox.warning(self, "错误", f"重置数据失败: {str(e)}")
            finally:
                db.close()
                
    # 在AddProductDialog类后添加新的对话框类
    
    class AddAdminDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowIcon(get_app_icon())
            self.init_ui()
        
        def init_ui(self):
            self.setWindowTitle("添加管理员")
            self.setMinimumWidth(400)
            
            layout = QVBoxLayout()
            
            # 用户名
            username_layout = QHBoxLayout()
            username_label = QLabel("用户名:")
            self.username_input = QLineEdit()
            username_layout.addWidget(username_label)
            username_layout.addWidget(self.username_input)
            layout.addLayout(username_layout)
            
            # 密码
            password_layout = QHBoxLayout()
            password_label = QLabel("密码:")
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.Password)
            password_layout.addWidget(password_label)
            password_layout.addWidget(self.password_input)
            layout.addLayout(password_layout)
            
            # 权限设置
            permissions_group = QGroupBox("权限设置")
            permissions_layout = QVBoxLayout()
            
            self.ban_permission = QCheckBox("封禁用户权限")
            self.modify_points_permission = QCheckBox("修改用户积分权限")
            self.delete_user_permission = QCheckBox("删除用户权限")
            self.manage_products_permission = QCheckBox("管理商品权限")
            self.manage_orders_permission = QCheckBox("管理订单权限")
            self.manage_admins_permission = QCheckBox("管理其他管理员权限")
            
            permissions_layout.addWidget(self.ban_permission)
            permissions_layout.addWidget(self.modify_points_permission)
            permissions_layout.addWidget(self.delete_user_permission)
            permissions_layout.addWidget(self.manage_products_permission)
            permissions_layout.addWidget(self.manage_orders_permission)
            permissions_layout.addWidget(self.manage_admins_permission)
            
            permissions_group.setLayout(permissions_layout)
            layout.addWidget(permissions_group)
            
            # 按钮
            button_layout = QHBoxLayout()
            ok_button = QPushButton("确定")
            ok_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            ok_button.clicked.connect(self.accept)
            cancel_button = QPushButton("取消")
            cancel_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(ok_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)
            
            self.setLayout(layout)
            
        def get_permissions(self):
            """获取选中的权限"""
            permissions = {
                'ban_users': self.ban_permission.isChecked(),
                'modify_points': self.modify_points_permission.isChecked(),
                'delete_users': self.delete_user_permission.isChecked(),
                'manage_products': self.manage_products_permission.isChecked(),
                'manage_orders': self.manage_orders_permission.isChecked(),
                'manage_admins': self.manage_admins_permission.isChecked()
            }
            return permissions

# 在AdminView类中添加以下方法

    def create_admin(self):
        dialog = self.AddAdminDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            username = dialog.username_input.text()
            password = dialog.password_input.text()
            permissions = dialog.get_permissions()
            
            if not username or not password:
                QMessageBox.warning(self, "错误", "请填写用户名和密码")
                return
                
            success, message = create_admin_user(username, password, permissions)
            if success:
                QMessageBox.information(self, "成功", message)
                self.load_users()  # 刷新用户列表
            else:
                QMessageBox.warning(self, "错误", message)

    def closeEvent(self, event):
        self.session.close()

    def generate_invite_code(self):
        from models.invite_code import PrivilegeType
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton
        
        # 创建特权选择对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("生成邀请码")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        # 特权类型选择
        privilege_layout = QHBoxLayout()
        privilege_layout.addWidget(QLabel("特权类型:"))
        
        privilege_combo = QComboBox()
        privilege_combo.addItem("普通用户", PrivilegeType.NORMAL)
        privilege_combo.addItem("VIP用户", PrivilegeType.VIP)
        # 移除管理员邀请码选项，管理员只能由超级管理员后台创建
        privilege_layout.addWidget(privilege_combo)
        
        layout.addLayout(privilege_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        confirm_btn = QPushButton("生成")
        cancel_btn = QPushButton("取消")
        
        button_layout.addWidget(confirm_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        # 按钮事件
        def on_confirm():
            selected_privilege = privilege_combo.currentData()
            invite_code = create_invite_code(selected_privilege)
            if invite_code:
                QMessageBox.information(self, "成功", f"邀请码生成成功: {invite_code.code}\n特权类型: {privilege_combo.currentText()}")
                self.load_invite_codes()
                dialog.accept()
            else:
                QMessageBox.warning(self, "错误", "邀请码生成失败")
        
        confirm_btn.clicked.connect(on_confirm)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec_()

    def load_invite_codes(self):
        invite_codes = get_invite_codes()
        self.invite_code_table.setRowCount(len(invite_codes))
        for i, code in enumerate(invite_codes):
            self.invite_code_table.setItem(i, 0, QTableWidgetItem(code.code))
            
            # 特权类型显示
            privilege_names = {
                "normal": "普通用户",
                "vip": "VIP用户", 
                "admin": "管理员"
            }
            privilege_text = privilege_names.get(code.privilege_type.value if hasattr(code.privilege_type, 'value') else str(code.privilege_type), "未知")
            self.invite_code_table.setItem(i, 1, QTableWidgetItem(privilege_text))
            
            self.invite_code_table.setItem(i, 2, QTableWidgetItem("已使用" if code.is_used else "未使用"))
            self.invite_code_table.setItem(i, 3, QTableWidgetItem(str(code.created_at)))
            if code.is_used:
                btn = QPushButton("删除")
                btn.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 6px;")
                btn.clicked.connect(lambda _, cid=code.id: self.delete_invite_code_dialog(cid))
                self.invite_code_table.setCellWidget(i, 4, btn)
            else:
                self.invite_code_table.setCellWidget(i, 4, None)
        self.invite_code_table.setColumnCount(5)
        self.invite_code_table.setHorizontalHeaderLabels(["邀请码", "特权类型", "状态", "创建时间", "操作"])

    def delete_invite_code_dialog(self, invite_id):
        reply = QMessageBox.question(
            self,
            "确认删除",
            "确定要删除该已使用的邀请码吗？此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if delete_invite_code(invite_id):
                QMessageBox.information(self, "成功", "邀请码已删除")
                self.load_invite_codes()
            else:
                QMessageBox.warning(self, "错误", "删除邀请码失败")

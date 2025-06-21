from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from plugins.plugin_manager import PluginManager

class PluginManagerView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.plugin_manager = PluginManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f8fa;
            }
            QPushButton {
                background-color: #4CAF50;
                color: #fff;
                border: none;
                border-radius: 6px;
                padding: 10px 0;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        # 插件管理
        plugin_layout = QVBoxLayout()
        plugin_title = QLabel("插件管理")
        plugin_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #222; margin-bottom: 20px;")
        plugin_title.setAlignment(Qt.AlignCenter)
        plugin_layout.addWidget(plugin_title)
        install_button = QPushButton("安装插件")
        install_button.clicked.connect(self.install_plugin)
        plugin_layout.addWidget(install_button)
        self.plugin_table = QTableWidget()
        self.plugin_table.setColumnCount(3)
        self.plugin_table.setHorizontalHeaderLabels(["插件名称", "版本", "描述"])
        plugin_layout.addWidget(self.plugin_table)
        layout.addLayout(plugin_layout)
        self.setLayout(layout)
        self.load_plugins()

    def install_plugin(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择插件文件", "", "Python Files (*.py)")
        if file_name:
            if self.plugin_manager.install_plugin(file_name):
                QMessageBox.information(self, "成功", "插件安装成功")
                self.load_plugins()
            else:
                QMessageBox.warning(self, "错误", "插件安装失败")

    def load_plugins(self):
        self.plugin_table.setRowCount(0)
        for plugin_name in self.plugin_manager.plugins:
            info = self.plugin_manager.get_plugin_info(plugin_name)
            if info:
                row = self.plugin_table.rowCount()
                self.plugin_table.insertRow(row)
                self.plugin_table.setItem(row, 0, QTableWidgetItem(info["name"]))
                self.plugin_table.setItem(row, 1, QTableWidgetItem(info["version"]))
                self.plugin_table.setItem(row, 2, QTableWidgetItem(info["description"])) 
from PyQt5.QtGui import QIcon
import os

def get_icon_path(icon_name):
    """获取图标的相对路径"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "..", "assets", "icons", f"{icon_name}.ico")

def get_app_icon():
    """获取应用程序图标"""
    return QIcon(get_icon_path("store_shop"))

def get_icon(icon_name):
    """获取指定名称的图标"""
    return QIcon(get_icon_path(icon_name))
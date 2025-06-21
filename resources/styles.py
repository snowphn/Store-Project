"""
通用UI样式定义
包含按钮、输入框、对话框等组件的统一样式
"""

# 统一按钮样式
UNIFIED_BUTTON_STYLE = """
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
    font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #5a6fd8, stop:1 #6a4190);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
QPushButton:pressed {
    transform: translateY(0px);
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4a5bc4, stop:1 #5a3580);
}
QPushButton:disabled {
    background: #cccccc;
    color: #666666;
    transform: none;
    box-shadow: none;
}
"""

# 主要操作按钮样式（绿色）
PRIMARY_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4CAF50, stop:1 #45a049);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: bold;
    min-height: 20px;
    font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #45a049, stop:1 #3d8b40);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}
QPushButton:pressed {
    transform: translateY(0px);
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3d8b40, stop:1 #357a38);
}
"""

# 危险操作按钮样式（红色）
DANGER_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #e74c3c, stop:1 #c0392b);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: bold;
    min-height: 20px;
    font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #c0392b, stop:1 #a93226);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
}
QPushButton:pressed {
    transform: translateY(0px);
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #a93226, stop:1 #922b21);
}
"""

# 次要操作按钮样式（灰色）
SECONDARY_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #6c757d, stop:1 #545b62);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: bold;
    min-height: 20px;
    font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #545b62, stop:1 #495057);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(108, 117, 125, 0.3);
}
QPushButton:pressed {
    transform: translateY(0px);
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #495057, stop:1 #3d4449);
}
"""

# 管理员专用按钮样式（紫色）
ADMIN_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #9b59b6, stop:1 #8e44ad);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: bold;
    min-height: 20px;
    font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #8e44ad, stop:1 #7d3c98);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(142, 68, 173, 0.3);
}
QPushButton:pressed {
    transform: translateY(0px);
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #7d3c98, stop:1 #6c3483);
}
"""

# 统一输入框样式
UNIFIED_INPUT_STYLE = """
QLineEdit {
    padding: 12px;
    border: 2px solid #dee2e6;
    border-radius: 8px;
    font-size: 14px;
    background: white;
    font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
}
QLineEdit:focus {
    border-color: #667eea;
    box-shadow: 0 0 5px rgba(102,126,234,0.3);
}
QLineEdit:hover {
    border-color: #adb5bd;
}
"""

# 统一对话框样式
UNIFIED_DIALOG_STYLE = """
QDialog {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f8f9fa, stop:1 #e9ecef);
    border-radius: 12px;
    font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
}
QLabel {
    color: #495057;
    font-size: 14px;
}
"""

# 获取样式的便捷函数
def get_button_style(button_type="default"):
    """获取指定类型的按钮样式"""
    styles = {
        "default": UNIFIED_BUTTON_STYLE,
        "primary": PRIMARY_BUTTON_STYLE,
        "danger": DANGER_BUTTON_STYLE,
        "secondary": SECONDARY_BUTTON_STYLE,
        "admin": ADMIN_BUTTON_STYLE
    }
    return styles.get(button_type, UNIFIED_BUTTON_STYLE)

def get_input_style():
    """获取输入框样式"""
    return UNIFIED_INPUT_STYLE

def get_dialog_style():
    """获取对话框样式"""
    return UNIFIED_DIALOG_STYLE
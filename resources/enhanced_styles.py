"""
增强版UI样式 - 专门用于美化留白区域
"""

def get_enhanced_background_style():
    """获取增强版背景样式"""
    return """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #667eea, stop:0.3 #764ba2, stop:0.7 #f093fb, stop:1 #f5576c);
        }
        
        QWidget {
            font-family: 'Microsoft YaHei UI', 'Segoe UI', Arial, sans-serif;
        }
        
        /* 装饰性背景元素 */
        QFrame#decorative_bg {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(255,255,255,0.1), stop:1 rgba(255,255,255,0.05));
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        /* 浮动装饰圆圈 */
        QLabel#floating_circle {
            background: qradial-gradient(circle, 
                rgba(255,255,255,0.15) 0%, 
                rgba(255,255,255,0.05) 70%, 
                transparent 100%);
            border-radius: 50px;
        }
        
        /* 网格装饰背景 */
        QFrame#grid_bg {
            background-image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48cGF0dGVybiBpZD0iZ3JpZCIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBwYXR0ZXJuVW5pdHM9InVzZXJTcGFjZU9uVXNlIj48cGF0aCBkPSJNIDQwIDAgTCAwIDAgMCA0MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMSkiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==);
        }
    """

def get_enhanced_content_style():
    """获取增强版内容区域样式"""
    return """
        /* 主要内容框架 */
        QFrame#main_content {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255,255,255,0.95), 
                stop:0.5 rgba(255,255,255,0.9), 
                stop:1 rgba(255,255,255,0.85));
            border-radius: 20px;
            border: 2px solid rgba(255,255,255,0.3);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        
        /* 导航栏美化 */
        QFrame#nav_frame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255,255,255,0.9), 
                stop:1 rgba(255,255,255,0.8));
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.4);
            margin: 10px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        /* 内容区域美化 */
        QFrame#content_frame {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255,255,255,0.95), 
                stop:1 rgba(248,250,252,0.9));
            border-radius: 15px;
            margin: 10px;
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        /* 产品卡片美化 */
        QFrame#product_card {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(255,255,255,0.95), 
                stop:1 rgba(248,250,252,0.9));
            border-radius: 15px;
            border: 2px solid rgba(255,255,255,0.4);
            margin: 8px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }
        
        QFrame#product_card:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(255,255,255,1), 
                stop:1 rgba(248,250,252,0.95));
            border: 2px solid rgba(102,126,234,0.3);
            transform: translateY(-2px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.12);
        }
        
        /* 滚动区域美化 */
        QScrollArea {
            border: none;
            background: transparent;
            border-radius: 10px;
        }
        
        QScrollBar:vertical {
            background: rgba(255,255,255,0.3);
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }
        
        QScrollBar::handle:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea, stop:1 #764ba2);
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #5a6fd8, stop:1 #6a4190);
        }
    """

def get_floating_elements_style():
    """获取浮动装饰元素样式"""
    return """
        /* 浮动装饰元素 */
        QLabel#floating_dot_1 {
            background: qradial-gradient(circle, 
                rgba(102,126,234,0.3) 0%, 
                rgba(102,126,234,0.1) 50%, 
                transparent 100%);
            border-radius: 30px;
        }
        
        QLabel#floating_dot_2 {
            background: qradial-gradient(circle, 
                rgba(118,75,162,0.3) 0%, 
                rgba(118,75,162,0.1) 50%, 
                transparent 100%);
            border-radius: 25px;
        }
        
        QLabel#floating_dot_3 {
            background: qradial-gradient(circle, 
                rgba(240,147,251,0.3) 0%, 
                rgba(240,147,251,0.1) 50%, 
                transparent 100%);
            border-radius: 20px;
        }
        
        /* 波浪装饰 */
        QFrame#wave_decoration {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255,255,255,0.2), 
                stop:0.5 rgba(255,255,255,0.1), 
                stop:1 rgba(255,255,255,0.2));
            border-radius: 50px;
        }
    """

def create_floating_decorations(parent_widget):
    """创建浮动装饰元素"""
    from PyQt5.QtWidgets import QLabel
    from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, pyqtProperty
    from PyQt5.QtGui import QPainter, QColor
    import random
    
    decorations = []
    
    # 创建多个浮动圆点
    for i in range(6):
        dot = QLabel(parent_widget)
        dot.setObjectName(f"floating_dot_{(i % 3) + 1}")
        
        # 随机大小和位置
        size = random.randint(40, 80)
        dot.setFixedSize(size, size)
        
        # 随机初始位置
        x = random.randint(0, parent_widget.width() - size)
        y = random.randint(0, parent_widget.height() - size)
        dot.move(x, y)
        
        decorations.append(dot)
        dot.show()
    
    return decorations

def animate_floating_elements(decorations, parent_widget):
    """为浮动元素添加动画"""
    from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, QEasingCurve
    import random
    
    def move_decoration(decoration):
        # 创建移动动画
        animation = QPropertyAnimation(decoration, b"geometry")
        animation.setDuration(random.randint(3000, 6000))
        
        # 当前位置
        current_rect = decoration.geometry()
        
        # 新的随机位置
        new_x = random.randint(0, parent_widget.width() - decoration.width())
        new_y = random.randint(0, parent_widget.height() - decoration.height())
        new_rect = QRect(new_x, new_y, decoration.width(), decoration.height())
        
        animation.setStartValue(current_rect)
        animation.setEndValue(new_rect)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        
        # 动画完成后继续下一个动画
        animation.finished.connect(lambda: move_decoration(decoration))
        animation.start()
        
        return animation
    
    # 为每个装饰元素启动动画
    animations = []
    for decoration in decorations:
        animation = move_decoration(decoration)
        animations.append(animation)
    
    return animations
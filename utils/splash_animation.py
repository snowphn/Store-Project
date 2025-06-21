import sys
import math
from PyQt5.QtWidgets import QSplashScreen, QLabel, QProgressBar, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, QEasingCurve, pyqtProperty, Qt
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QLinearGradient, QColor, QFont, QMovie
import random
from resources.icons import get_icon_path

class AnimatedSplashScreen(QSplashScreen):
    def __init__(self):
        # 创建透明背景
        pixmap = QPixmap(500, 350)
        pixmap.fill(Qt.transparent)
        super().__init__(pixmap)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        # 初始化动画组件
        self.setup_ui()
        self.setup_animations()
        self.setup_particles()
        
        # 动画状态
        self.animation_step = 0
        self.gradient_offset = 0
        
    def setup_ui(self):
        """设置UI组件"""
        # 主容器
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 500, 350)
        
        # Logo标签
        self.logo_label = QLabel(self.container)
        self.logo_label.setGeometry(200, 80, 100, 100)
        self.logo_label.setAlignment(Qt.AlignCenter)
        
        # 尝试加载图标
        try:
            logo_pixmap = QPixmap(get_icon_path("store_shop"))
            if not logo_pixmap.isNull():
                scaled_pixmap = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_label.setPixmap(scaled_pixmap)
            else:
                self.logo_label.setText("🏪")
                self.logo_label.setStyleSheet("font-size: 48px;")
        except:
            self.logo_label.setText("🏪")
            self.logo_label.setStyleSheet("font-size: 48px;")
        
        # 标题标签
        self.title_label = QLabel("Hurricane Community Store", self.container)
        self.title_label.setGeometry(50, 200, 400, 40)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Microsoft YaHei';
            }
        """)
        
        # 状态标签
        self.status_label = QLabel("正在启动...", self.container)
        self.status_label.setGeometry(50, 250, 400, 30)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 180);
                font-size: 14px;
                font-family: 'Microsoft YaHei';
            }
        """)
        
        # 进度条
        self.progress_bar = QProgressBar(self.container)
        self.progress_bar.setGeometry(100, 290, 300, 8)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: rgba(255, 255, 255, 30);
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:0.5 #667eea, stop:1 #764ba2);
                border-radius: 4px;
            }
        """)
        
    def setup_animations(self):
        """设置动画"""
        # Logo旋转动画
        self.logo_rotation = QPropertyAnimation(self.logo_label, b"rotation")
        self.logo_rotation.setDuration(3000)
        self.logo_rotation.setStartValue(0)
        self.logo_rotation.setEndValue(360)
        self.logo_rotation.setEasingCurve(QEasingCurve.InOutSine)
        self.logo_rotation.setLoopCount(-1)  # 无限循环
        
        # 标题淡入淡出动画
        self.title_fade = QPropertyAnimation(self.title_label, b"opacity")
        self.title_fade.setDuration(2000)
        self.title_fade.setStartValue(0.5)
        self.title_fade.setEndValue(1.0)
        self.title_fade.setEasingCurve(QEasingCurve.InOutSine)
        
        # 背景渐变动画定时器
        self.gradient_timer = QTimer()
        self.gradient_timer.timeout.connect(self.update_gradient)
        self.gradient_timer.start(50)  # 每50ms更新一次
        
        # 粒子动画定时器
        self.particle_timer = QTimer()
        self.particle_timer.timeout.connect(self.update_particles)
        self.particle_timer.start(100)  # 每100ms更新一次
        
    def setup_particles(self):
        """设置粒子效果"""
        self.particles = []
        for i in range(15):
            particle = {
                'x': random.randint(0, 500),
                'y': random.randint(0, 350),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'size': random.randint(2, 6),
                'opacity': random.uniform(0.3, 0.8)
            }
            self.particles.append(particle)
    
    def update_gradient(self):
        """更新背景渐变"""
        self.gradient_offset = (self.gradient_offset + 1) % 360
        self.update()
    
    def update_particles(self):
        """更新粒子位置"""
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # 边界检测
            if particle['x'] < 0 or particle['x'] > 500:
                particle['vx'] *= -1
            if particle['y'] < 0 or particle['y'] > 350:
                particle['vy'] *= -1
                
            # 保持在边界内
            particle['x'] = max(0, min(500, particle['x']))
            particle['y'] = max(0, min(350, particle['y']))
        
        self.update()
    
    def paintEvent(self, event):
        """自定义绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制动态渐变背景
        gradient = QLinearGradient(0, 0, 500, 350)
        
        # 计算动态颜色
        offset = self.gradient_offset / 360.0
        color1 = QColor.fromHsv(int(240 + offset * 60) % 360, 200, 230)
        color2 = QColor.fromHsv(int(280 + offset * 60) % 360, 180, 200)
        color3 = QColor.fromHsv(int(320 + offset * 60) % 360, 160, 180)
        
        gradient.setColorAt(0, color1)
        gradient.setColorAt(0.5, color2)
        gradient.setColorAt(1, color3)
        
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # 绘制粒子
        painter.setPen(Qt.NoPen)
        for particle in self.particles:
            color = QColor(255, 255, 255, int(particle['opacity'] * 255))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(
                int(particle['x']), int(particle['y']),
                particle['size'], particle['size']
            )
        
        # 绘制光晕效果
        center_x, center_y = 250, 175
        for i in range(3):
            radius = 100 + i * 50
            opacity = 30 - i * 10
            color = QColor(255, 255, 255, opacity)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(
                center_x - radius, center_y - radius,
                radius * 2, radius * 2
            )
    
    def start_animations(self):
        """启动所有动画"""
        self.logo_rotation.start()
        self.title_fade.start()
    
    def update_progress(self, value, message=""):
        """更新进度和状态消息"""
        self.progress_bar.setValue(value)
        if message:
            self.status_label.setText(message)
    
    def finish_animation(self):
        """完成动画"""
        self.gradient_timer.stop()
        self.particle_timer.stop()
        self.logo_rotation.stop()

def show_splash_screen():
    """显示启动动画"""
    # 加载启动图片
    logo_pixmap = QPixmap(get_icon_path("store_shop"))
    splash = QSplashScreen(logo_pixmap)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.show()
    
    # 设置定时器，2秒后关闭启动画面
    QTimer.singleShot(2000, splash.close)
    
    return splash
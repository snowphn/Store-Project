from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QBrush, QLinearGradient
import random
import math

class AnimatedBackground(QWidget):
    """动态背景效果组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(50)  # 20 FPS
        
        # 创建粒子
        self.create_particles()
    
    def create_particles(self):
        """创建背景粒子"""
        for _ in range(20):
            particle = {
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'size': random.randint(2, 8),
                'opacity': random.uniform(0.1, 0.3),
                'color': random.choice([
                    QColor(102, 126, 234, int(255 * 0.2)),
                    QColor(118, 75, 162, int(255 * 0.2)),
                    QColor(240, 147, 251, int(255 * 0.2))
                ])
            }
            self.particles.append(particle)
    
    def update_particles(self):
        """更新粒子位置"""
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # 边界检测
            if particle['x'] < 0 or particle['x'] > self.width():
                particle['vx'] *= -1
            if particle['y'] < 0 or particle['y'] > self.height():
                particle['vy'] *= -1
        
        self.update()
    
    def paintEvent(self, event):
        """绘制粒子"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for particle in self.particles:
            painter.setBrush(QBrush(particle['color']))
            painter.setPen(particle['color'])
            painter.drawEllipse(
                int(particle['x']), 
                int(particle['y']), 
                particle['size'], 
                particle['size']
            )
    
    def resizeEvent(self, event):
        """窗口大小改变时重新创建粒子"""
        super().resizeEvent(event)
        self.particles.clear()
        self.create_particles()
from PIL import Image, ImageDraw, ImageFont
import random
import string
import io
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray
import os
from PIL import Image, ImageDraw, ImageFont

class CaptchaGenerator:
    def __init__(self, width=160, height=70):
        self.width = width
        self.height = height
        self.font_size = 12
        # 定义安全裁剪区域，确保验证码完全在此区域内
        self.safe_margin_x = 20  # 左右安全边距
        self.safe_margin_y = 15  # 上下安全边距
        self.safe_width = self.width - 2 * self.safe_margin_x  # 安全区域宽度
        self.safe_height = self.height - 2 * self.safe_margin_y  # 安全区域高度
        
    def generate_code(self):
        """生成随机4位数字验证码"""
        return ''.join([str(random.randint(0, 9)) for _ in range(4)])
    
    def create_image(self, code):
        """创建验证码图片"""
        # 创建图片
        image = Image.new('RGB', (self.width, self.height), color='white')
        draw = ImageDraw.Draw(image)
        
        # 尝试加载字体，如果失败则使用默认字体
        try:
            # Windows系统字体路径
            font_path = "C:/Windows/Fonts/arial.ttf"
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, self.font_size)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # 绘制背景干扰线
        for _ in range(5):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            draw.line([(x1, y1), (x2, y2)], fill=self._random_color(150, 200), width=1)
        
        # 绘制干扰点
        for _ in range(50):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.point((x, y), fill=self._random_color(100, 200))
        
        # 绘制验证码文字 - 完全居中显示
        # 估算字符尺寸（基于字体大小）
        char_estimated_width = self.font_size * 0.7  # 字符宽度约为字体大小的70%
        char_estimated_height = self.font_size  # 字符高度约等于字体大小
        
        # 计算整个验证码的总宽度
        total_text_width = char_estimated_width * 4 + 10 * 5  # 4个字符 + 3个间隔
        
        # 计算起始X位置，使整个验证码水平居中
        start_x = (self.width - total_text_width) // 2
        
        # 计算垂直居中位置
        center_y = (self.height - char_estimated_height) // 2
        
        for i, char in enumerate(code):
            # 计算基础位置 - 水平和垂直都居中
            base_x = start_x + i * (char_estimated_width + 5)  # 字符间距为10像素
            base_y = center_y
            
            # 计算安全的随机偏移范围，保持居中效果
            max_x_offset = 2  # 减小随机偏移，保持居中效果
            max_y_offset = 2
            
            # 应用随机偏移
            x_offset = random.randint(-max_x_offset, max_x_offset)
            y_offset = random.randint(-max_y_offset, max_y_offset)
            
            x = base_x + x_offset
            y = base_y + y_offset
            
            # 边界检查 - 确保字符不超出图像边界
            x = max(0, min(x, self.width - char_estimated_width))
            y = max(0, min(y, self.height - char_estimated_height))
            
            color = self._random_color(0, 100)
            draw.text((x, y), char, font=font, fill=color)
        
        return image
    
    def _random_color(self, min_val=0, max_val=255):
        """生成随机颜色"""
        return (random.randint(min_val, max_val),
                random.randint(min_val, max_val),
                random.randint(min_val, max_val))
    
    def image_to_qpixmap(self, image):
        """将PIL图片转换为QPixmap"""
        # 将PIL图片转换为字节流
        byte_array = io.BytesIO()
        image.save(byte_array, format='PNG')
        byte_array.seek(0)
        
        # 转换为QPixmap
        qbyte_array = QByteArray(byte_array.read())
        pixmap = QPixmap()
        pixmap.loadFromData(qbyte_array)
        
        return pixmap
    
    def generate_captcha(self):
        """生成验证码和对应的图片"""
        code = self.generate_code()
        image = self.create_image(code)
        pixmap = self.image_to_qpixmap(image)
        return code, pixmap
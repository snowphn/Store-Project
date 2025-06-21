from PIL import Image
import io
import base64
import os
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QBuffer

def qimage_to_bytes(qimage, fmt="PNG"):
    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    qimage.save(buffer, fmt)
    return buffer.data().data()

def compress_image(image_data, max_size=(200, 200), quality=85):
    """压缩图片
    
    Args:
        image_data: 图片数据（字节或QImage）
        max_size: 最大尺寸 (宽, 高)
        quality: JPEG压缩质量 (1-100)
        
    Returns:
        压缩后的图片数据（字节）
    """
    # 如果是QImage，转换为PIL Image
    if isinstance(image_data, QImage):
        image_data = qimage_to_bytes(image_data)
    # 打开图片
    img = Image.open(io.BytesIO(image_data))
    # 转换为RGB模式（如果是RGBA）
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    # 调整大小
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    # 保存为JPEG
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    return output.getvalue()

def save_avatar(image_data, user_id):
    """保存用户头像
    
    Args:
        image_data: 图片数据（字节或QImage）
        user_id: 用户ID
        
    Returns:
        头像文件名
    """
    # 确保目录存在
    avatar_dir = os.path.join("assets", "avatars")
    os.makedirs(avatar_dir, exist_ok=True)
    
    # 压缩图片
    compressed_data = compress_image(image_data)
    
    # 生成文件名
    filename = f"avatar_{user_id}.jpg"
    filepath = os.path.join(avatar_dir, filename)
    
    # 保存文件
    with open(filepath, "wb") as f:
        f.write(compressed_data)
        
    return filename

def load_avatar(filename):
    """加载用户头像
    
    Args:
        filename: 文件名
        
    Returns:
        图片数据（字节）或None
    """
    filepath = os.path.join("assets", "avatars", filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return f.read()
    return None

def image_to_base64(image_data):
    """将图片数据转换为Base64编码
    
    Args:
        image_data: 图片数据（字节）
        
    Returns:
        Base64编码的字符串
    """
    return base64.b64encode(image_data).decode('utf-8')

def base64_to_image(base64_str):
    """将Base64编码转换为图片数据
    
    Args:
        base64_str: Base64编码的字符串
        
    Returns:
        图片数据（字节）
    """
    return base64.b64decode(base64_str)

def qimage_to_pixmap(qimage, size=None):
    """将QImage转换为QPixmap
    
    Args:
        qimage: QImage对象
        size: 目标大小 (宽, 高)
        
    Returns:
        QPixmap对象
    """
    pixmap = QPixmap.fromImage(qimage)
    if size:
        pixmap = pixmap.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return pixmap 
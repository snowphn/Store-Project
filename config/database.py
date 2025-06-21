import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csgo_shop.db')

# 构建数据库URL
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Steam API配置
STEAM_API_KEY = os.getenv('STEAM_API_KEY', '658DF34B878A55239139EA6507722DF2')

# 支付接口配置
PAYMENT_API_KEY = os.getenv('PAYMENT_API_KEY', 'test_api_key')
PAYMENT_API_URL = os.getenv('PAYMENT_API_URL', 'https://api.payment.example.com')
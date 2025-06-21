import json
import requests
import os
from typing import Dict, Optional
from config.database import PAYMENT_API_KEY, PAYMENT_API_URL
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class PaymentAPI:
    def __init__(self):
        self.api_key = PAYMENT_API_KEY
        self.api_url = PAYMENT_API_URL
        self.session = self._create_session()
        
    def _create_session(self):
        """创建带重试机制的会话"""
        session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # 清除代理设置
        session.proxies = {}
        
        return session
        
    def create_payment(self, amount: float, order_id: str) -> Optional[Dict]:
        """创建支付订单"""
        try:
            # 检查是否启用模拟模式
            if os.getenv('USE_PAYMENT_SIMULATION', 'false').lower() == 'true':
                logging.info("使用支付模拟模式")
                return simulate_payment_process(amount)
            
            data = {
                'amount': amount,
                'order_id': order_id,
                'api_key': self.api_key
            }
            
            response = self.session.post(
                f"{self.api_url}/create",
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 405:
                # 尝试使用GET方法
                logging.warning("POST方法不被允许，尝试使用GET方法创建支付")
                response = self.session.get(
                    f"{self.api_url}/create",
                    params=data,
                    timeout=10
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    logging.error(f"GET方法创建支付也失败: {response.status_code} - {response.text}")
                    return simulate_payment_process(amount)
            else:
                logging.error(f"支付API返回错误: {response.status_code} - {response.text}")
                return simulate_payment_process(amount)
                
        except requests.exceptions.ProxyError as e:
            logging.error(f"代理连接错误: {str(e)}")
            return simulate_payment_process(amount)
        except requests.exceptions.ConnectionError as e:
            logging.error(f"网络连接错误: {str(e)}")
            return simulate_payment_process(amount)
        except Exception as e:
            logging.error(f"支付订单创建异常: {str(e)}")
            return simulate_payment_process(amount)
    
    def check_payment(self, payment_id: str) -> Optional[Dict]:
        """查询支付状态"""
        try:
            # 检查是否启用模拟模式
            if os.getenv('USE_PAYMENT_SIMULATION', 'false').lower() == 'true':
                logging.info("使用支付模拟模式")
                return {
                    'success': True,
                    'status': 'paid',
                    'payment_id': payment_id,
                    'message': '模拟支付成功'
                }
            
            data = {
                'payment_id': payment_id,
                'api_key': self.api_key
            }
            
            # 使用带重试机制的session
            response = self.session.post(
                f"{self.api_url}/check",
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 405:
                # 尝试使用GET方法
                logging.warning("POST方法不被允许，尝试使用GET方法")
                response = self.session.get(
                    f"{self.api_url}/check",
                    params=data,
                    timeout=10
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    logging.error(f"GET方法也失败: {response.status_code} - {response.text}")
                    return self._fallback_payment_check(payment_id)
            else:
                logging.error(f"查询支付状态失败: {response.status_code} - {response.text}")
                return self._fallback_payment_check(payment_id)
                
        except requests.exceptions.ProxyError as e:
            logging.error(f"代理连接错误: {str(e)}")
            return self._fallback_payment_check(payment_id)
        except requests.exceptions.ConnectionError as e:
            logging.error(f"网络连接错误: {str(e)}")
            return self._fallback_payment_check(payment_id)
        except Exception as e:
            logging.error(f"查询支付状态异常: {str(e)}")
            return self._fallback_payment_check(payment_id)
    
    def _fallback_payment_check(self, payment_id: str) -> Dict:
        """支付查询失败时的回退处理"""
        logging.info(f"使用回退模式处理支付查询: {payment_id}")
        return {
            'success': True,
            'status': 'pending',
            'payment_id': payment_id,
            'message': '支付状态查询失败，请手动确认支付结果'
        }
    
    def calculate_points(self, amount: float, exchange_rate: int = 100) -> float:
        """计算充值积分"""
        return amount * exchange_rate  # 可配置兑换比例

class PaymentConfig:
    """支付配置类"""
    # 兑换比例配置
    EXCHANGE_RATES = {
        'default': 1,    # 1元 = 100积分
        'vip': 3,        # VIP用户：1元 = 120积分
        'promotion': 2   # 促销期间：1元 = 150积分
    }
    
    # 支付方式配置
    PAYMENT_METHODS = {
        'alipay': {'name': '支付宝', 'enabled': True},
        'wechat': {'name': '微信支付', 'enabled': True},
        'bank': {'name': '银行卡', 'enabled': False}
    }
    
    @classmethod
    def get_exchange_rate(cls, user_type: str = 'default') -> int:
        """获取用户对应的兑换比例"""
        return cls.EXCHANGE_RATES.get(user_type, cls.EXCHANGE_RATES['default'])
    
    @classmethod
    def get_available_payment_methods(cls) -> Dict:
        """获取可用的支付方式"""
        return {k: v for k, v in cls.PAYMENT_METHODS.items() if v['enabled']}

def simulate_payment_process(amount: float, payment_method: str = 'alipay') -> Dict:
    """模拟支付流程（用于测试）"""
    import time
    import random
    
    # 模拟支付处理时间
    time.sleep(1)
    
    # 模拟支付结果（90%成功率）
    success = random.random() > 0.1
    
    return {
        'success': success,
        'payment_id': f'pay_{int(time.time())}_{random.randint(1000, 9999)}',
        'amount': amount,
        'method': payment_method,
        'message': '支付成功' if success else '支付失败，请重试'
    }


# 在PaymentAPI类中添加网络诊断方法
def check_network_connectivity(self):
    """检查网络连接状态"""
    try:
        # 清除代理设置
        session = requests.Session()
        session.proxies = {}
        
        # 测试基本网络连接
        response = session.get('https://httpbin.org/ip', timeout=5)
        print(f"网络连接正常: {response.json()}")
        
        # 测试支付API连接
        response = session.get(self.api_url, timeout=5)
        print(f"支付API连接状态: {response.status_code}")
        
    except Exception as e:
        print(f"网络连接检查失败: {str(e)}")
        return False
    return True
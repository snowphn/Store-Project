import os
import json
import hmac
import hashlib
import base64
import time
import requests
from urllib.parse import urlencode, parse_qs
from config.database import STEAM_API_KEY

class SteamWebLogin:
    def __init__(self):
        self.api_key = STEAM_API_KEY
        self.base_url = "https://steamcommunity.com"
        self.api_url = "https://api.steampowered.com"
        self.session = requests.Session()
        
    def get_login_url(self, return_url: str) -> str:
        """获取Steam登录URL"""
        return_url = "https://cnhvh.com/steam/callback"
        realm = "https://cnhvh.com"
        params = {
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.mode': 'checkid_setup',
            'openid.return_to': return_url,
            'openid.realm': realm,
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select'
        }
        
        return f"{self.base_url}/openid/login?{urlencode(params)}"
    
    def verify_login(self, params: dict) -> dict:
        """验证Steam登录回调"""
        try:
            # 添加必要的参数
            params['openid.mode'] = 'check_authentication'
            params['openid.ns'] = 'http://specs.openid.net/auth/2.0'
            
            # 发送验证请求
            response = requests.post(f"{self.base_url}/openid/login", data=params)
            
            if 'is_valid:true' in response.text:
                # 从claimed_id中提取steam_id
                steam_id = params['openid.claimed_id'].split('/')[-1]
                
                # 获取用户信息
                user_info = self.get_user_info(steam_id)
                if user_info:
                    return {
                        'steam_id': steam_id,
                        'name': user_info.get('personaname'),
                        'avatar': user_info.get('avatarfull'),
                        'profile_url': user_info.get('profileurl')
                    }
            
            return None
        except Exception as e:
            print(f"验证Steam登录失败: {str(e)}")
            return None
    
    def get_user_info(self, steam_id: str) -> dict:
        """获取Steam用户信息"""
        try:
            url = f"{self.api_url}/ISteamUser/GetPlayerSummaries/v0002/"
            params = {
                'key': self.api_key,
                'steamids': steam_id
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data['response']['players']:
                    return data['response']['players'][0]
            return None
        except Exception as e:
            print(f"获取Steam用户信息失败: {str(e)}")
            return None
    
    def parse_openid_response(self, query_string: str) -> dict:
        """解析OpenID响应"""
        try:
            # 解析查询字符串
            params = parse_qs(query_string)
            
            # 将列表值转换为单个值
            return {k: v[0] if isinstance(v, list) else v for k, v in params.items()}
        except Exception as e:
            print(f"解析OpenID响应失败: {str(e)}")
            return None
    
    def generate_session_id(self) -> str:
        """生成会话ID"""
        return base64.b64encode(os.urandom(32)).decode('utf-8')
    
    def validate_session(self, session_id: str, steam_id: str) -> bool:
        """验证会话"""
        try:
            # 这里可以添加会话验证逻辑
            # 例如检查会话是否过期，是否与steam_id匹配等
            return True
        except Exception:
            return False 
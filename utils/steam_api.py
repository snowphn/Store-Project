import requests
from typing import Dict, Optional
from config.database import STEAM_API_KEY

class SteamAPI:
    def __init__(self):
        self.api_key = STEAM_API_KEY
        self.base_url = "https://api.steampowered.com"
    
    def get_player_info(self, steam_id: str) -> Optional[Dict]:
        """获取Steam玩家信息"""
        try:
            # 确保steam_id是64位格式
            if not steam_id.isdigit():
                steam_id = self.convert_to_steam64(steam_id)
                if not steam_id:
                    return None
            
            # 使用Steam Web API获取玩家信息
            url = f"{self.base_url}/ISteamUser/GetPlayerSummaries/v0002/"
            params = {
                'key': self.api_key,
                'steamids': steam_id
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data['response']['players']:
                    player = data['response']['players'][0]
                    return {
                        'steam_id': player['steamid'],
                        'name': player['personaname'],
                        'avatar': player['avatarfull'],
                        'profile_url': player['profileurl'],
                        'last_online': player.get('lastlogoff', 0)
                    }
            return None
        except Exception as e:
            print(f"获取Steam玩家信息失败: {str(e)}")
            return None
    
    def convert_to_steam64(self, steam_id: str) -> Optional[str]:
        """将Steam ID转换为64位格式"""
        try:
            # 处理STEAM_X:Y:Z格式
            if steam_id.startswith('STEAM_'):
                parts = steam_id.split(':')
                if len(parts) == 3:
                    y = int(parts[1])
                    z = int(parts[2])
                    return str(z * 2 + y + 76561197960265728)
            
            # 处理[U:1:XXXXXX]格式
            if steam_id.startswith('[U:1:'):
                steam_id = steam_id[5:-1]
                return str(int(steam_id) + 76561197960265728)
            
            # 处理社区URL
            if 'steamcommunity.com' in steam_id:
                # 从URL中提取steamid
                if '/profiles/' in steam_id:
                    steam_id = steam_id.split('/profiles/')[-1].split('/')[0]
                elif '/id/' in steam_id:
                    # 需要额外的API调用来获取steamid
                    vanity_url = steam_id.split('/id/')[-1].split('/')[0]
                    steam_id = self.get_steam_id_from_vanity_url(vanity_url)
            
            return steam_id if steam_id.isdigit() else None
        except Exception:
            return None
    
    def get_steam_id_from_vanity_url(self, vanity_url: str) -> Optional[str]:
        """从自定义URL获取Steam ID"""
        try:
            url = f"{self.base_url}/ISteamUser/ResolveVanityURL/v0001/"
            params = {
                'key': self.api_key,
                'vanityurl': vanity_url
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data['response']['success'] == 1:
                    return data['response']['steamid']
            return None
        except Exception as e:
            print(f"获取Steam ID失败: {str(e)}")
            return None
    
    def validate_steam_id(self, steam_id: str) -> bool:
        """验证Steam ID是否有效"""
        player_info = self.get_player_info(steam_id)
        return player_info is not None
    
    def get_player_owned_games(self, steam_id: str) -> Optional[Dict]:
        """获取玩家拥有的游戏列表"""
        try:
            url = f"{self.base_url}/IPlayerService/GetOwnedGames/v0001/"
            params = {
                'key': self.api_key,
                'steamid': steam_id,
                'include_appinfo': 1,
                'include_played_free_games': 1
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"获取玩家游戏列表失败: {str(e)}")
            return None
    
    def get_player_friends(self, steam_id: str) -> Optional[Dict]:
        """获取玩家的好友列表"""
        try:
            url = f"{self.base_url}/ISteamUser/GetFriendList/v0001/"
            params = {
                'key': self.api_key,
                'steamid': steam_id,
                'relationship': 'friend'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"获取好友列表失败: {str(e)}")
            return None 
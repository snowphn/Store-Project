import a2s
import socket
import time
from typing import Dict, Optional, Tuple, List


class CSGOServer:
    def __init__(self, ip: str, port: int = 27015):
        """初始化CSGO服务器查询器
        
        Args:
            ip: 服务器IP地址
            port: 服务器端口，默认27015
        """
        self.ip = ip
        self.port = port
        self.address = (ip, port)
    
    @classmethod
    def from_address_string(cls, address_str: str):
        """从地址字符串创建实例
        
        Args:
            address_str: 格式如 '192.168.1.1:27015' 或 '192.168.1.1'
        """
        if ':' in address_str:
            ip, port = address_str.rsplit(':', 1)  # 使用rsplit防止IPv6问题
            return cls(ip, int(port))
        else:
            return cls(address_str)
    
    @staticmethod
    def parse_address(address_str: str) -> Optional[Tuple[str, int]]:
        """解析服务器地址字符串
        
        Args:
            address_str: 服务器地址字符串，格式如 '192.168.1.1:27015' 或 '192.168.1.1'
            
        Returns:
            包含IP和端口的元组，解析失败时返回None
        """
        try:
            if ':' in address_str:
                ip, port = address_str.rsplit(':', 1)
                return (ip.strip(), int(port))
            else:
                return (address_str.strip(), 27015)  # 默认端口
        except (ValueError, AttributeError):
            return None
    
    def get_server_info(self) -> Optional[Dict]:
        """获取服务器信息"""
        try:
            start_time = time.time()
            
            # 获取服务器基本信息 - 修复：使用self.address而不是server
            info = a2s.info(self.address, timeout=5.0)
            
            # 计算ping时间
            ping = round((time.time() - start_time) * 1000)
            
            # 获取玩家信息
            try:
                players = a2s.players(self.address, timeout=5.0)
                player_count = len(players)
            except (socket.timeout, a2s.BrokenMessageError):
                player_count = info.player_count
                players = []
            
            return {
                '服务器名称': info.server_name,
                '地图': info.map_name,
                '玩家数量': player_count,
                '最大玩家数': info.max_players,
                '延迟': ping,
                'IP地址': self.ip,
                '端口': self.port,
                '游戏': info.folder,
                '版本': info.version,
                '协议': info.protocol,
                '玩家列表': [{'姓名': p.name, '分数': p.score, '游戏时长': p.duration} for p in players]
            }
        except (socket.timeout, ConnectionRefusedError, a2s.BrokenMessageError, OSError) as e:
            print(f"查询服务器失败 {self.ip}:{self.port}: {str(e)}")
            return None
    
    def __str__(self) -> str:
        return f"CSGOServer({self.ip}:{self.port})"
    
    def __repr__(self) -> str:
        return f"CSGOServer(ip='{self.ip}', port={self.port})"

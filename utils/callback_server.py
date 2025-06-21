from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading
import json
import os

class SteamCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理GET请求"""
        try:
            # 解析URL参数
            query = urlparse(self.path).query
            params = parse_qs(query)
            
            # 将列表值转换为单个值
            params = {k: v[0] if isinstance(v, list) else v for k, v in params.items()}
            
            # 保存回调参数
            with open('steam_callback.json', 'w', encoding='utf-8') as f:
                json.dump(params, f)
            
            # 发送成功响应
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # 返回成功页面
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Steam Login Success</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background-color: #171a21;
                        color: #ffffff;
                    }
                    .container {
                        text-align: center;
                        padding: 20px;
                        background-color: #2a3f5f;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0,0,0,0.5);
                    }
                    h1 {
                        color: #66c0f4;
                    }
                    p {
                        margin: 20px 0;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Steam Login Success</h1>
                    <p>You can close this window and return to the application.</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
            
        except Exception as e:
            print(f"处理回调请求失败: {str(e)}")
            self.send_error(500, "Internal Server Error")
    
    def log_message(self, format, *args):
        """禁用日志输出"""
        pass

def start_callback_server(port=8000):
    """启动回调服务器"""
    try:
        server = HTTPServer(('localhost', port), SteamCallbackHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        return server
    except Exception as e:
        print(f"启动回调服务器失败: {str(e)}")
        return None

def stop_callback_server(server):
    """停止回调服务器"""
    if server:
        try:
            server.shutdown()
            server.server_close()
        except Exception as e:
            print(f"停止回调服务器失败: {str(e)}")

def get_callback_params():
    """获取回调参数"""
    try:
        if os.path.exists('steam_callback.json'):
            with open('steam_callback.json', 'r', encoding='utf-8') as f:
                params = json.load(f)
            os.remove('steam_callback.json')  # 删除文件
            return params
    except Exception as e:
        print(f"获取回调参数失败: {str(e)}")
    return None 
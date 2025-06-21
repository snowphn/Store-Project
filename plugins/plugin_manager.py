import os
import importlib.util
import json
from typing import Dict, Any

class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, Any] = {}
        self.load_plugins()

    def load_plugins(self):
        """加载所有插件"""
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py"):
                plugin_name = filename[:-3]
                self.load_plugin(plugin_name)

    def load_plugin(self, plugin_name: str):
        """加载单个插件"""
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, os.path.join(self.plugin_dir, f"{plugin_name}.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.plugins[plugin_name] = module
            print(f"插件 {plugin_name} 加载成功")
        except Exception as e:
            print(f"插件 {plugin_name} 加载失败: {str(e)}")

    def install_plugin(self, plugin_file: str):
        """安装新插件"""
        try:
            plugin_name = os.path.basename(plugin_file).split(".")[0]
            target_path = os.path.join(self.plugin_dir, f"{plugin_name}.py")
            with open(plugin_file, "r") as f:
                content = f.read()
            with open(target_path, "w") as f:
                f.write(content)
            self.load_plugin(plugin_name)
            return True
        except Exception as e:
            print(f"插件安装失败: {str(e)}")
            return False

    def uninstall_plugin(self, plugin_name: str):
        """卸载插件"""
        try:
            if plugin_name in self.plugins:
                del self.plugins[plugin_name]
                os.remove(os.path.join(self.plugin_dir, f"{plugin_name}.py"))
                print(f"插件 {plugin_name} 卸载成功")
                return True
            return False
        except Exception as e:
            print(f"插件卸载失败: {str(e)}")
            return False

    def get_plugin_info(self, plugin_name: str) -> Dict[str, Any]:
        """获取插件信息"""
        if plugin_name in self.plugins:
            return {
                "name": plugin_name,
                "version": getattr(self.plugins[plugin_name], "version", "unknown"),
                "description": getattr(self.plugins[plugin_name], "description", "No description")
            }
        return None 
from flask import Flask, request, jsonify
from plugins.plugin_manager import PluginManager
import os

app = Flask(__name__)
plugin_manager = PluginManager()

@app.route("/api/plugins", methods=["GET"])
def list_plugins():
    """获取所有插件信息"""
    plugins = []
    for plugin_name in plugin_manager.plugins:
        info = plugin_manager.get_plugin_info(plugin_name)
        if info:
            plugins.append(info)
    return jsonify(plugins)

@app.route("/api/plugins/install", methods=["POST"])
def install_plugin():
    """安装新插件"""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith(".py"):
        file_path = os.path.join(plugin_manager.plugin_dir, file.filename)
        file.save(file_path)
        if plugin_manager.install_plugin(file_path):
            return jsonify({"message": "Plugin installed successfully"})
        return jsonify({"error": "Plugin installation failed"}), 500
    return jsonify({"error": "Invalid file type"}), 400

@app.route("/api/plugins/<plugin_name>", methods=["DELETE"])
def uninstall_plugin(plugin_name):
    """卸载插件"""
    if plugin_manager.uninstall_plugin(plugin_name):
        return jsonify({"message": "Plugin uninstalled successfully"})
    return jsonify({"error": "Plugin uninstallation failed"}), 500

if __name__ == "__main__":
    app.run(debug=True) 
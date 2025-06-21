# 开发者API文档

本文档详细说明所有API接口及其用法，帮助开发者开发插件。

## 插件管理API

### 获取所有插件信息
- **接口**: `GET /api/plugins`
- **描述**: 返回所有已安装插件的名称、版本、描述等信息。
- **返回示例**:
  ```json
  [
    {
      "name": "invite_code",
      "version": "1.0.0",
      "description": "邀请码管理插件"
    }
  ]
  ```

### 安装新插件
- **接口**: `POST /api/plugins/install`
- **描述**: 接收上传的插件文件（.py），自动安装并加载。
- **请求参数**:
  - `file`: 插件文件（.py）
- **返回示例**:
  ```json
  {
    "message": "Plugin installed successfully"
  }
  ```

### 卸载插件
- **接口**: `DELETE /api/plugins/<plugin_name>`
- **描述**: 根据插件名称卸载插件。
- **返回示例**:
  ```json
  {
    "message": "Plugin uninstalled successfully"
  }
  ```

## 插件开发指南

1. **插件文件结构**  
   - 插件文件必须为 `.py` 格式，放在 `plugins` 目录下。
   - 插件文件必须包含 `version`、`description` 变量，以及 `get_plugin_info()` 函数。

2. **插件API示例**  
   - 插件文件示例（`plugins/invite_code_plugin.py`）:
     ```python
     version = "1.0.0"
     description = "邀请码管理插件"

     def get_plugin_info():
         return {
             "name": "invite_code",
             "version": version,
             "description": description
         }

     def install():
         pass

     def uninstall():
         pass

     # 插件API
     def generate_code():
         return create_invite_code()

     def list_codes():
         return get_invite_codes()

     def verify_code(code):
         return use_invite_code(code)
     ```

3. **插件安装/卸载**  
   - 通过API上传插件文件，系统自动安装。
   - 通过API卸载插件，系统自动清理。

## 其他说明

- 插件文件必须符合系统要求，否则无法加载。
- 插件API可根据需求扩展，系统自动加载。 
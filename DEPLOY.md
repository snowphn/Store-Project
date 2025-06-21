# Hurricane.exe部署说明

## 环境要求

- Python 3.8+
- MySQL 5.7+
- Windows 10/11

## 安装步骤

1. 克隆代码仓库
```bash
git clone <repository_url>
cd csgo-shop
```

2. 创建虚拟环境
```bash
python -m venv venv
venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
- 复制 `.env.example` 为 `.env`
- 修改 `.env` 中的配置信息：
  - 数据库连接信息
  - Steam API密钥
  - 支付接口配置

5. 初始化数据库
```bash
python -c "from database.db_init import init_database; init_database()"
```

6. 运行应用
```bash
python main.py
```

## 数据库配置

1. 创建MySQL数据库
```sql
CREATE DATABASE csgo_shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 创建数据库用户并授权
```sql
CREATE USER 'csgo_shop'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON csgo_shop.* TO 'csgo_shop'@'localhost';
FLUSH PRIVILEGES;
```

## 支付接口配置

1. 申请支付接口账号
2. 获取API密钥
3. 在 `.env` 文件中配置支付接口信息

## Steam API配置

1. 访问 https://steamcommunity.com/dev/apikey
2. 申请API密钥
3. 在 `.env` 文件中配置Steam API密钥

## 注意事项

1. 确保MySQL服务已启动
2. 检查防火墙设置，确保应用可以访问网络
3. 定期备份数据库
4. 保护好API密钥和数据库密码

## 常见问题

1. 数据库连接失败
   - 检查数据库服务是否启动
   - 验证数据库连接信息是否正确

2. Steam API调用失败
   - 确认API密钥是否有效
   - 检查网络连接

3. 支付接口异常
   - 验证API密钥是否正确
   - 检查支付接口服务是否可用 
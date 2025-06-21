# Hurricane Community Store

A modern CS:GO community store application built with PyQt5, featuring a comprehensive shop system, user management, and Steam integration.
Admin User:123
Admin Password:111
## 🚀 Features

### Core Features
- **User Management**: Registration, login, and profile management
- **Product Catalog**: Browse and purchase CS:GO items
- **Shopping Cart**: Add items and manage purchases
- **Order System**: Complete order processing and history
- **Admin Panel**: Comprehensive administration tools
- **Steam Integration**: Steam account binding and authentication

### Advanced Features
- **Payment System**: Integrated payment processing
- **Invite Code System**: Referral and invitation management
- **Points System**: User rewards and loyalty points
- **Plugin System**: Extensible plugin architecture
- **CS:GO Server Integration**: Direct server communication
- **Modern UI**: Beautiful and responsive user interface

## 🛠️ Technology Stack

- **Frontend**: PyQt5 with custom styling
- **Backend**: Python with SQLAlchemy ORM
- **Database**: SQLite (configurable to MySQL)
- **Authentication**: Custom user authentication system
- **Payment**: Integrated payment gateway support
- **Steam API**: Steam Web API integration

## 📋 Requirements

- Python 3.7+
- PyQt5
- SQLAlchemy
- Other dependencies listed in `requirements.txt`

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hurricane-community-store.git
   cd hurricane-community-store
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Initialize the database**
   ```bash
   python database/db_init.py
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_URL=sqlite:///csgo_shop.db

# Steam API Configuration
STEAM_API_KEY=your_steam_api_key

# Payment Configuration
PAYMENT_GATEWAY_URL=your_payment_gateway_url
PAYMENT_API_KEY=your_payment_api_key

# Application Settings
DEBUG=false
USE_PAYMENT_SIMULATION=true
```

### Default Admin Account

The application creates a default admin account on first run:
- **Username**: `123`
- **Password**: `111`
- **Email**: `admin@hurricane.com`

**⚠️ Important**: Change the default admin credentials immediately after first login!

## 📖 Usage

### For Users
1. **Registration**: Create a new account or login with existing credentials
2. **Browse Products**: Explore the available CS:GO items
3. **Shopping**: Add items to cart and proceed to checkout
4. **Steam Binding**: Link your Steam account for enhanced features
5. **Order History**: View your purchase history and order status

### For Administrators
1. **Admin Panel**: Access comprehensive administration tools
2. **Product Management**: Add, edit, and manage store products
3. **User Management**: Manage user accounts and permissions
4. **Order Management**: Process and track customer orders
5. **System Settings**: Configure application settings and plugins

## 🔌 Plugin System

The application supports a flexible plugin system:

- **Invite Code Plugin**: Manage referral systems
- **Custom Plugins**: Develop your own plugins using the plugin API

See the `plugins/` directory for examples and documentation.

## 🗂️ Project Structure

```
├── api/                    # API endpoints
├── assets/                 # Static assets (icons, images)
├── config/                 # Configuration files
├── controllers/            # Business logic controllers
├── database/               # Database operations and migrations
├── docs/                   # Documentation
├── models/                 # Data models
├── plugins/                # Plugin system
├── resources/              # UI resources and styles
├── utils/                  # Utility functions
├── views/                  # UI views and components
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [documentation](docs/)
2. Search existing [issues](https://github.com/yourusername/hurricane-community-store/issues)
3. Create a new issue if needed

## 🙏 Acknowledgments

- PyQt5 community for the excellent GUI framework
- Steam Web API for integration capabilities
- All contributors who helped improve this project

## 📊 Development Status

- ✅ Core functionality implemented
- ✅ User management system
- ✅ Product and order management
- ✅ Payment system integration
- ✅ Steam API integration
- 🔄 Plugin system enhancements
- 🔄 Additional payment gateways
- 📋 Mobile companion app (planned)

---

**Made with ❤️ by Hurricane Team**

---

# Hurricane 社区商店

一个基于 PyQt5 构建的现代化 CS:GO 社区商店应用程序，具有完整的商店系统、用户管理和 Steam 集成功能。

管理员账号:123
管理员密码:111

## 🚀 功能特性

### 核心功能
- **用户管理**: 注册、登录和个人资料管理
- **商品目录**: 浏览和购买 CS:GO 物品
- **购物车**: 添加商品并管理购买
- **订单系统**: 完整的订单处理和历史记录
- **管理面板**: 全面的管理工具
- **Steam 集成**: Steam 账户绑定和认证

### 高级功能
- **支付系统**: 集成支付处理
- **邀请码系统**: 推荐和邀请管理
- **积分系统**: 用户奖励和忠诚度积分
- **插件系统**: 可扩展的插件架构
- **CS:GO 服务器集成**: 直接服务器通信
- **现代化界面**: 美观且响应式的用户界面

## 🛠️ 技术栈

- **前端**: PyQt5 自定义样式
- **后端**: Python 与 SQLAlchemy ORM
- **数据库**: SQLite（可配置为 MySQL）
- **认证**: 自定义用户认证系统
- **支付**: 集成支付网关支持
- **Steam API**: Steam Web API 集成

## 📋 系统要求

- Python 3.7+
- PyQt5
- SQLAlchemy
- 其他依赖项请参见 `requirements.txt`

## 🚀 安装指南

1. **克隆仓库**
   ```bash
   git clone https://github.com/yourusername/hurricane-community-store.git
   cd hurricane-community-store
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **设置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件配置您的设置
   ```

5. **初始化数据库**
   ```bash
   python database/db_init.py
   ```

6. **运行应用程序**
   ```bash
   python main.py
   ```

## ⚙️ 配置说明

### 环境变量

在根目录创建 `.env` 文件并配置以下变量：

```env
# 数据库配置
DATABASE_URL=sqlite:///csgo_shop.db

# Steam API 配置
STEAM_API_KEY=your_steam_api_key

# 支付配置
PAYMENT_GATEWAY_URL=your_payment_gateway_url
PAYMENT_API_KEY=your_payment_api_key

# 应用程序设置
DEBUG=false
USE_PAYMENT_SIMULATION=true
```

### 默认管理员账户

应用程序首次运行时会创建默认管理员账户：
- **用户名**: `123`
- **密码**: `111`
- **邮箱**: `admin@hurricane.com`

**⚠️ 重要**: 首次登录后请立即更改默认管理员凭据！

## 📖 使用说明

### 普通用户
1. **注册**: 创建新账户或使用现有凭据登录
2. **浏览商品**: 探索可用的 CS:GO 物品
3. **购物**: 将物品添加到购物车并结账
4. **Steam 绑定**: 绑定您的 Steam 账户以获得增强功能
5. **订单历史**: 查看您的购买历史和订单状态

### 管理员
1. **管理面板**: 访问全面的管理工具
2. **商品管理**: 添加、编辑和管理商店商品
3. **用户管理**: 管理用户账户和权限
4. **订单管理**: 处理和跟踪客户订单
5. **系统设置**: 配置应用程序设置和插件

## 🔌 插件系统

应用程序支持灵活的插件系统：

- **邀请码插件**: 管理推荐系统
- **自定义插件**: 使用插件 API 开发您自己的插件

请参阅 `plugins/` 目录获取示例和文档。

## 🗂️ 项目结构

```
├── api/                    # API 端点
├── assets/                 # 静态资源（图标、图片）
├── config/                 # 配置文件
├── controllers/            # 业务逻辑控制器
├── database/               # 数据库操作和迁移
├── docs/                   # 文档
├── models/                 # 数据模型
├── plugins/                # 插件系统
├── resources/              # UI 资源和样式
├── utils/                  # 工具函数
├── views/                  # UI 视图和组件
├── main.py                 # 应用程序入口点
├── requirements.txt        # Python 依赖
└── README.md              # 本文件
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详情请参见 [LICENSE](LICENSE) 文件。

## 🆘 技术支持

如果您遇到任何问题或有疑问：

1. 查看[文档](docs/)
2. 搜索现有[问题](https://github.com/yourusername/hurricane-community-store/issues)
3. 如需要请创建新问题

## 🙏 致谢

- PyQt5 社区提供的优秀 GUI 框架
- Steam Web API 的集成能力
- 所有帮助改进此项目的贡献者

## 📊 开发状态

- ✅ 核心功能已实现
- ✅ 用户管理系统
- ✅ 商品和订单管理
- ✅ 支付系统集成
- ✅ Steam API 集成
- 🔄 插件系统增强
- 🔄 额外支付网关
- 📋 移动端配套应用（计划中）

---

**由 Hurricane 团队用 ❤️ 制作**

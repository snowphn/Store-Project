# 支付功能配置说明

## 概述

本系统已经从模拟支付升级为真实支付接口。用户必须完成真实的扫码支付才能成功充值积分。

## 主要改进

### 1. 移除模拟支付
- 删除了 `simulate_payment_process` 函数的调用
- 不再使用随机成功率的模拟支付
- 用户必须完成真实支付才能获得积分

### 2. 真实支付流程
- 创建真实的支付订单
- 生成支付二维码供用户扫描
- 实时查询支付状态
- 只有支付成功才会增加用户积分

### 3. 用户体验优化
- 显示支付进度条
- 提供二维码支付界面
- 支持取消支付操作
- 支付超时提醒

## 配置步骤

### 1. 环境变量配置

复制 `.env.example` 文件为 `.env`，并配置以下参数：

```bash
# 支付接口配置
PAYMENT_API_KEY=your_real_payment_api_key
PAYMENT_API_URL=https://your-payment-provider.com/api
```

### 2. 支付接口要求

您的支付接口需要提供以下API端点：

#### 创建支付订单
- **URL**: `POST {PAYMENT_API_URL}/create`
- **请求参数**:
  ```json
  {
    "amount": 100.00,
    "order_id": "order_1234567890_abcd1234",
    "api_key": "your_api_key"
  }
  ```
- **响应格式**:
  ```json
  {
    "payment_id": "pay_1234567890",
    "qr_code_url": "https://payment-url-for-qr-code",
    "status": "pending"
  }
  ```

#### 查询支付状态
- **URL**: `POST {PAYMENT_API_URL}/check`
- **请求参数**:
  ```json
  {
    "payment_id": "pay_1234567890",
    "api_key": "your_api_key"
  }
  ```
- **响应格式**:
  ```json
  {
    "status": "success",  // success, failed, pending
    "message": "支付成功",
    "amount": 100.00
  }
  ```

### 3. 支持的支付方式

当前支持以下支付方式：
- 支付宝
- 微信支付
- 银行卡（可在配置中启用/禁用）

### 4. 安全特性

- API密钥通过环境变量配置，不会硬编码在代码中
- 支付状态通过服务器端验证
- 支持支付超时处理
- 用户可以随时取消支付

## 测试建议

### 1. 开发环境测试

在开发环境中，建议使用支付接口的沙箱环境进行测试：

```bash
PAYMENT_API_URL=https://sandbox-api.payment-provider.com/api
PAYMENT_API_KEY=sandbox_test_key
```

### 2. 生产环境部署

在生产环境中，确保使用真实的支付接口：

```bash
PAYMENT_API_URL=https://api.payment-provider.com/api
PAYMENT_API_KEY=production_api_key
```

## 常见问题

### Q: 支付接口返回错误怎么办？
A: 检查以下几点：
1. API密钥是否正确
2. 网络连接是否正常
3. 支付接口URL是否正确
4. 请求参数格式是否符合要求

### Q: 二维码无法生成怎么办？
A: 确保已安装 `qrcode` 依赖：
```bash
pip install qrcode[pil]
```

### Q: 支付状态查询超时怎么办？
A: 系统会在5分钟后超时，用户可以：
1. 联系客服确认支付状态
2. 稍后查看账户余额
3. 重新发起支付

## 技术支持

如需技术支持，请提供以下信息：
1. 错误日志
2. 支付订单号
3. 支付时间
4. 支付金额

---

**注意**: 请确保在生产环境中使用真实的支付接口，并妥善保管API密钥。
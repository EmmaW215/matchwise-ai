# Render 配置检查清单

## 📋 必需的环境变量

根据代码分析，以下环境变量**必须**在 Render 中配置：

### 1. **XAI_API_KEY** ⚠️ 必需
- **用途**: xAI Grok API 密钥，用于 AI 文本生成（备用服务）
- **如何获取**: 从 xAI 开发者平台获取
- **检查**: 确保值不为空，格式正确

### 2. **OPENAI_API_KEY** ⚠️ 必需
- **用途**: OpenAI API 密钥，用于 AI 文本生成（主要服务）
- **如何获取**: 从 OpenAI 平台获取
- **检查**: 确保值不为空，格式以 `sk-` 开头

### 3. **STRIPE_SECRET_KEY** ⚠️ 必需
- **用途**: Stripe 支付服务密钥
- **如何获取**: 从 Stripe Dashboard → Developers → API keys
- **检查**: 确保是 Secret Key（不是 Publishable Key），以 `sk_` 开头

### 4. **STRIPE_WEBHOOK_SECRET** ⚠️ 必需
- **用途**: Stripe Webhook 签名密钥，用于验证 webhook 请求
- **如何获取**: 从 Stripe Dashboard → Developers → Webhooks → 选择 webhook → Signing secret
- **检查**: 确保值不为空，格式为 `whsec_...`

---

## 🔧 可选的环境变量

### 5. **ALLOWED_ORIGINS** (可选)
- **用途**: 额外的允许跨域访问的前端域名
- **格式**: 多个域名用逗号分隔，例如：
  ```
  https://smartsuccess-ai.vercel.app,https://another-domain.com
  ```
- **默认值**: 代码中已包含以下默认域名：
  - `https://resume-matcher-frontend.vercel.app`
  - `https://resume-update-frontend.vercel.app`
  - `https://matchwise-ai.vercel.app`
  - `http://localhost:3000`
  - `http://localhost:3001`

---

## 🔥 Firebase 配置

### 6. **serviceAccountKey.json** ⚠️ 必需文件
- **用途**: Firebase Admin SDK 服务账户密钥文件
- **位置**: 必须在 `resume-matcher-backend/` 目录中
- **如何获取**: 
  1. 访问 Firebase Console
  2. Project Settings → Service Accounts
  3. 点击 "Generate new private key"
  4. 下载 JSON 文件
  5. 重命名为 `serviceAccountKey.json`
  6. 上传到 Render 或通过环境变量配置

**⚠️ 重要**: 如果使用环境变量方式，需要将 JSON 内容转换为环境变量格式。

---

## ✅ Render 设置检查步骤

### 步骤 1: 检查环境变量

访问：https://dashboard.render.com/web/srv-d1h696jipnbc73bfhovg/settings

在 **Environment** 标签页中，确认以下变量已设置：

- [ ] `XAI_API_KEY` - 已设置且不为空
- [ ] `OPENAI_API_KEY` - 已设置且不为空
- [ ] `STRIPE_SECRET_KEY` - 已设置且不为空
- [ ] `STRIPE_WEBHOOK_SECRET` - 已设置且不为空
- [ ] `ALLOWED_ORIGINS` - 已设置（如果需要额外域名）

### 步骤 2: 检查服务设置

在 **Settings** 标签页中，检查：

#### Build & Deploy
- [ ] **Build Command**: 应该是 `pip install -r requirements.txt` 或留空（自动检测）
- [ ] **Start Command**: 应该是 `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] **Environment**: 应该是 `Python 3`

#### Health Check
- [ ] **Health Check Path**: 可以设置为 `/health`
- [ ] **Health Check Interval**: 建议设置为 60 秒

### 步骤 3: 检查文件结构

确保以下文件存在于 `resume-matcher-backend/` 目录：

- [ ] `main.py` - 主应用文件
- [ ] `requirements.txt` - Python 依赖
- [ ] `serviceAccountKey.json` - Firebase 服务账户密钥（或通过环境变量配置）

### 步骤 4: 检查 Git 连接

- [ ] **Repository**: 应该连接到 `https://github.com/EmmaW215/matchwise-ai`
- [ ] **Branch**: 应该是 `main`
- [ ] **Root Directory**: 应该是 `resume-matcher-backend`（如果项目在子目录中）

---

## 🧪 验证配置

### 测试 1: Health Check

```bash
curl https://resume-matcher-backend-rrrw.onrender.com/health
```

**预期响应**:
```json
{"status": "ok"}
```

### 测试 2: CORS 配置

从浏览器控制台或使用 curl 测试：

```bash
curl -X OPTIONS https://resume-matcher-backend-rrrw.onrender.com/api/compare \
  -H "Origin: https://matchwise-ai.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

应该返回 CORS 相关的 headers。

### 测试 3: API 端点

```bash
curl https://resume-matcher-backend-rrrw.onrender.com/
```

应该返回欢迎消息。

---

## 🐛 常见问题排查

### 问题 1: 服务无法启动

**可能原因**:
- 缺少必需的环境变量
- `serviceAccountKey.json` 文件缺失或格式错误
- Python 依赖安装失败

**解决方案**:
1. 检查 Render 日志：**Logs** 标签页
2. 确认所有环境变量已设置
3. 检查 `requirements.txt` 是否包含所有依赖

### 问题 2: CORS 错误

**可能原因**:
- 前端域名不在允许列表中
- `ALLOWED_ORIGINS` 格式错误

**解决方案**:
1. 检查前端域名是否在默认列表中
2. 如果不在，添加到 `ALLOWED_ORIGINS` 环境变量
3. 重新部署服务

### 问题 3: API 调用失败

**可能原因**:
- API 密钥无效或过期
- API 配额用尽
- 网络连接问题

**解决方案**:
1. 验证 API 密钥是否有效
2. 检查 API 使用配额
3. 查看 Render 日志中的具体错误信息

### 问题 4: Firebase 连接失败

**可能原因**:
- `serviceAccountKey.json` 文件缺失
- 文件内容格式错误
- Firebase 项目配置不匹配

**解决方案**:
1. 确认文件存在于正确位置
2. 验证 JSON 格式是否正确
3. 检查 Firebase 项目 ID 是否匹配

---

## 📝 环境变量设置示例

在 Render Dashboard 的 **Environment** 标签页中，应该看到类似这样的配置：

```
XAI_API_KEY=<your-xai-api-key>
OPENAI_API_KEY=<your-openai-api-key>
STRIPE_SECRET_KEY=<your-stripe-secret-key>
STRIPE_WEBHOOK_SECRET=<your-stripe-webhook-secret>
ALLOWED_ORIGINS=https://smartsuccess-ai.vercel.app
```

**注意**: 请将 `<your-...-key>` 替换为实际的 API 密钥值。

---

## 🔒 安全建议

1. **不要**在代码中硬编码 API 密钥
2. **使用**环境变量存储敏感信息
3. **定期**轮换 API 密钥
4. **限制** `ALLOWED_ORIGINS` 只包含必要的域名
5. **监控** API 使用情况，防止滥用

---

## 📞 需要帮助？

如果遇到问题：
1. 检查 Render 日志：**Logs** 标签页
2. 查看部署历史：**Events** 标签页
3. 验证环境变量：**Environment** 标签页
4. 检查服务状态：**Metrics** 标签页

---

**最后更新**: 2025年1月  
**服务 ID**: srv-d1h696jipnbc73bfhovg  
**服务 URL**: https://resume-matcher-backend-rrrw.onrender.com
# MatchWise AI 完整部署指南

## 🎯 部署前检查清单

### ✅ 前端（Vercel）配置

- [ ] **Root Directory** 已设置为 `resume-matcher-frontend`
- [ ] **Git 连接** 已连接到 `EmmaW215/matchwise-ai`
- [ ] **环境变量** 已配置：
  - [ ] `NEXT_PUBLIC_BACKEND_URL` - 后端 API URL
  - [ ] `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - Stripe 公钥（如果需要）
- [ ] **KV 数据库** 已连接：
  - [ ] `matchwise-kv-new` 数据库已创建
  - [ ] 数据库已连接到项目
  - [ ] `KV_REST_API_URL` 和 `KV_REST_API_TOKEN` 已自动配置
  - [ ] 旧的 `KV_URL` 和 `REDIS_URL` 已删除

### ✅ 后端（Render）配置

- [ ] **环境变量** 已配置：
  - [ ] `XAI_API_KEY` - xAI API 密钥
  - [ ] `OPENAI_API_KEY` - OpenAI API 密钥
  - [ ] `STRIPE_SECRET_KEY` - Stripe 密钥
  - [ ] `STRIPE_WEBHOOK_SECRET` - Stripe Webhook 密钥
  - [ ] `ALLOWED_ORIGINS` - 允许的前端域名（可选）
- [ ] **Firebase 配置**：
  - [ ] `serviceAccountKey.json` 文件已上传到 Render
  - [ ] 或通过环境变量配置

---

## 🚀 部署步骤

### 步骤 1: 提交所有更改到 GitHub

```bash
cd /Users/emmawang/Library/Mobile\ Documents/com~apple~CloudDocs/Emma\ My\ Product/AI_Projects/h_MatchWise_AI

# 添加所有文档文件
git add *.md

# 提交
git commit -m "docs: Add deployment and troubleshooting guides"

# 推送到 GitHub
git push origin main
```

### 步骤 2: 验证 Vercel 自动部署

1. **检查 GitHub 推送**
   - 访问：https://github.com/EmmaW215/matchwise-ai
   - 确认最新提交已推送

2. **检查 Vercel 部署**
   - 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments
   - 应该看到新的部署正在构建
   - 等待部署完成（通常 1-3 分钟）

3. **如果自动部署未触发**
   - 手动触发：点击 "Redeploy"

### 步骤 3: 验证前端部署

#### 检查部署状态

1. **访问部署页面**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments

2. **确认部署成功**
   - ✅ 状态为 "Ready"
   - ✅ 没有构建错误
   - ✅ 构建日志显示成功

#### 测试网站功能

访问部署后的 URL（通常在 Vercel Dashboard 的 "Domains" 部分显示）

测试功能：
- [ ] 页面正常加载
- [ ] 登录功能正常（Google Sign-In）
- [ ] 简历上传功能正常
- [ ] 访客计数器正常显示
- [ ] API 调用正常（生成分析功能）
- [ ] SmartSuccess.AI 集成功能正常（iframe 嵌入测试）

#### 检查日志

1. **访问函数日志**
   - 在部署详情页面，点击 "Functions" 标签
   - 检查 API 路由是否有错误

2. **测试访客计数器 API**
   - 访问：`https://your-domain.vercel.app/api/visitor-stats`
   - 应该返回 JSON 数据，没有错误

### 步骤 4: 验证后端部署（Render）

#### 检查后端状态

1. **访问 Render Dashboard**
   - https://dashboard.render.com/web/srv-d1h696jipnbc73bfhovg

2. **确认服务运行正常**
   - ✅ 状态为 "Live"
   - ✅ 没有错误日志

#### 测试后端 API

```bash
# 测试健康检查
curl https://resume-matcher-backend-rrrw.onrender.com/health

# 应该返回: {"status": "ok"}
```

#### 验证环境变量

1. **检查环境变量**
   - 在 Render Dashboard → Environment
   - 确认所有必需的环境变量已设置

2. **测试 API 端点**
   - 确认后端可以正常响应请求
   - 检查 CORS 配置是否正确

### 步骤 5: 端到端测试

#### 完整功能测试

1. **访问前端网站**
   - 打开部署后的 URL

2. **测试完整流程**
   - [ ] 上传简历文件
   - [ ] 输入职位描述
   - [ ] 点击 "Generate Comparison"
   - [ ] 等待分析完成
   - [ ] 查看结果（匹配分数、优化建议、求职信等）

3. **测试登录和订阅**
   - [ ] Google 登录功能
   - [ ] 用户状态查询
   - [ ] 订阅功能（如果需要）

4. **测试 SmartSuccess.AI 集成**
   - [ ] iframe 嵌入测试
   - [ ] postMessage 通信测试
   - [ ] 登录状态同步测试

---

## 🔍 验证清单

### 前端验证

- [ ] 部署状态为 "Ready"
- [ ] 网站可以正常访问
- [ ] 没有控制台错误
- [ ] 所有功能正常工作
- [ ] KV 数据库连接正常
- [ ] 环境变量配置正确

### 后端验证

- [ ] 服务状态为 "Live"
- [ ] Health check 返回正常
- [ ] API 端点可以访问
- [ ] CORS 配置正确
- [ ] 环境变量配置正确
- [ ] Firebase 连接正常

### 集成验证

- [ ] 前端可以调用后端 API
- [ ] 数据可以正常传输
- [ ] 错误处理正常
- [ ] 日志记录正常

---

## 🐛 如果遇到问题

### 前端问题

1. **构建失败**
   - 查看构建日志
   - 检查 TypeScript 错误
   - 确认依赖已安装

2. **运行时错误**
   - 检查浏览器控制台
   - 查看 Vercel 函数日志
   - 验证环境变量

3. **KV 连接错误**
   - 确认数据库已连接
   - 检查环境变量格式
   - 验证 API 密钥有效

### 后端问题

1. **服务无法启动**
   - 查看 Render 日志
   - 检查环境变量
   - 验证依赖安装

2. **API 调用失败**
   - 检查 CORS 配置
   - 验证 API 密钥
   - 查看错误日志

3. **Firebase 连接失败**
   - 确认 `serviceAccountKey.json` 存在
   - 验证 Firebase 配置

---

## 📊 部署后监控

### 监控指标

1. **Vercel Analytics**
   - 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/analytics
   - 查看访问量、性能等

2. **Render Metrics**
   - 访问 Render Dashboard
   - 查看服务指标

3. **错误日志**
   - 定期检查 Vercel 和 Render 日志
   - 及时发现和修复问题

---

## 🔗 重要链接

### 前端（Vercel）
- Dashboard: https://vercel.com/emma-wangs-projects/matchwise-ai-app
- 部署历史: https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments
- 环境变量: https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables
- Storage: https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/storage

### 后端（Render）
- Dashboard: https://dashboard.render.com/web/srv-d1h696jipnbc73bfhovg
- 环境变量: https://dashboard.render.com/web/srv-d1h696jipnbc73bfhovg/settings
- 日志: https://dashboard.render.com/web/srv-d1h696jipnbc73bfhovg/logs

### GitHub
- Repository: https://github.com/EmmaW215/matchwise-ai

---

## ✅ 最终检查清单

部署完成后，确认：

- [ ] 前端部署成功，网站可访问
- [ ] 后端服务运行正常，API 可访问
- [ ] 所有功能测试通过
- [ ] 没有错误日志
- [ ] 环境变量配置正确
- [ ] KV 数据库连接正常
- [ ] SmartSuccess.AI 集成功能正常

---

**恭喜！** 如果所有检查项都通过，你的项目已成功部署！🎉
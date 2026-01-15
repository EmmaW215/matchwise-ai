# 修复 Vercel KV 配置错误

## 🔴 错误信息

```
Upstash Redis client was passed an invalid URL. You should pass a URL starting with https. 
Received: "REDIS_URL="redis://default:lg3HbFsPTVlpKfUC43rNfKHhspynBNDJ@redis-13585.c262.us-east-1-3.ec2.redns.redis-cloud.com:13585""
```

## 🔍 问题分析

1. **环境变量格式错误**：`REDIS_URL` 的值包含了引号和变量名本身
2. **Vercel KV 需要 HTTPS URL**：`@vercel/kv` 需要 REST API URL（以 `https://` 开头），而不是直接的 Redis URL（`redis://`）

## ✅ 解决方案

### 方法 1: 使用 Vercel KV（推荐）

Vercel KV 会自动配置，不需要手动设置 `REDIS_URL`。

#### 步骤：

1. **访问 Vercel Dashboard**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/storage

2. **创建或检查 Vercel KV Store**
   - 如果还没有创建，点击 "Create Database"
   - 选择 "KV" (Key-Value)
   - 创建后会自动配置环境变量

3. **删除错误的 REDIS_URL 环境变量**
   - 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables
   - 找到 `REDIS_URL` 环境变量
   - **删除它**（Vercel KV 会自动配置正确的变量）

4. **确认自动配置的环境变量**
   Vercel KV 会自动创建以下环境变量（不需要手动设置）：
   - `KV_REST_API_URL` - REST API URL（以 https:// 开头）
   - `KV_REST_API_TOKEN` - API Token
   - `KV_URL` - 完整的连接 URL

### 方法 2: 如果使用外部 Redis（Upstash）

如果必须使用外部 Redis，需要设置正确的环境变量：

#### 步骤：

1. **访问 Vercel Dashboard**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables

2. **删除错误的 REDIS_URL**
   - 删除 `REDIS_URL` 环境变量

3. **添加正确的环境变量**
   从 Upstash Dashboard 获取：
   - **UPSTASH_REDIS_REST_URL**: `https://xxx.upstash.io`
   - **UPSTASH_REDIS_REST_TOKEN**: `your-token`

   **重要**：
   - 值应该是纯 URL/Token，**不要包含引号**
   - 值应该是纯文本，**不要包含变量名**

4. **环境变量格式示例**（正确）：
   ```
   UPSTASH_REDIS_REST_URL = https://xxx.upstash.io
   UPSTASH_REDIS_REST_TOKEN = AXXXAAItYjA...
   ```

   **错误格式**（不要这样做）：
   ```
   REDIS_URL = "REDIS_URL="redis://...""
   ```

## 🔧 快速修复步骤

### 步骤 1: 删除错误的环境变量

1. 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables
2. 找到 `REDIS_URL`
3. 点击删除按钮
4. 保存更改

### 步骤 2: 使用 Vercel KV（推荐）

1. 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/storage
2. 如果还没有 KV Store，创建 one
3. Vercel 会自动配置正确的环境变量

### 步骤 3: 重新部署

1. 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments
2. 点击最新的部署
3. 点击 "Redeploy"
4. 等待部署完成

## ✅ 验证修复

部署完成后，检查日志：

1. 访问部署日志
2. 查找 `/api/visitor-stats` 的调用
3. 应该看到：
   - ✅ `Successfully read visitor count from KV`
   - ✅ `Successfully updated visitor count in KV`
   - ❌ 不应该再看到 `invalid URL` 错误

## 📋 检查清单

- [ ] 删除了错误的 `REDIS_URL` 环境变量
- [ ] 创建了 Vercel KV Store（如果还没有）
- [ ] 确认 Vercel 自动配置了 `KV_REST_API_URL` 和 `KV_REST_API_TOKEN`
- [ ] 重新部署了应用
- [ ] 验证了日志中没有错误

## 🔗 相关链接

- Vercel KV 文档：https://vercel.com/docs/storage/vercel-kv
- 环境变量设置：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables
- Storage 设置：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/storage

---

**重要提示**：`@vercel/kv` 会自动从环境变量中读取配置，不需要手动设置 `REDIS_URL`。使用 Vercel KV 是最简单和推荐的方法。
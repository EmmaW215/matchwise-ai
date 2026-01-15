# 创建新的 Upstash KV 数据库 - 详细步骤

## 🎯 选择正确的选项

由于 Vercel 已将 KV 移至 Marketplace，你需要选择 **"Upstash"**。

## 📋 完整步骤

### 步骤 1: 选择 Upstash

在 "Browse Storage" 对话框中：

1. **找到 "Marketplace Database Providers" 部分**
2. **选择 "Upstash"**
   - 描述：`Serverless DB (Redis, Vector, Queue, Search)`
   - 这个选项提供 Redis/Key-Value 存储
3. **点击 "Continue"** 按钮（右下角黑色按钮）

### 步骤 2: 配置 Upstash 数据库

选择 Upstash 后，会进入配置页面：

1. **选择数据库类型**
   - 选择 **"Redis"** 或 **"KV"**（如果显示）
   - 这是 Key-Value 存储类型

2. **输入数据库名称**
   - 例如：`matchwise-kv` 或 `matchwise-kv-new`

3. **选择区域（Region）**
   - 选择离你最近的区域，例如：`US East (N. Virginia)`

4. **选择计划**
   - 选择 **"Free"** 计划（如果可用）

5. **点击 "Create"** 或 **"Continue"**

### 步骤 3: 连接到项目

创建数据库后：

1. **选择项目**
   - 选择 `matchwise-ai-app` 项目
   - 或选择你的 MatchWise AI 项目

2. **确认连接**
   - Vercel 会自动配置环境变量
   - 会添加：`KV_REST_API_URL`、`KV_REST_API_TOKEN` 等

3. **完成连接**

### 步骤 4: 验证环境变量

1. **访问环境变量设置**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables

2. **确认以下变量已自动添加：**
   - ✅ `KV_REST_API_URL` - 应该以 `https://` 开头
   - ✅ `KV_REST_API_TOKEN` - API 令牌
   - ✅ `KV_URL` - 完整的连接 URL（可选）

3. **删除旧的 REDIS_URL**（如果存在）
   - 找到 `REDIS_URL` 环境变量
   - 点击删除
   - Vercel KV 不需要这个变量

### 步骤 5: 重新部署

1. **访问部署页面**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments

2. **触发重新部署**
   - 点击最新部署的 "..." 菜单
   - 选择 "Redeploy"

3. **等待部署完成**

### 步骤 6: 验证修复

部署完成后，检查日志：

**应该看到：**
```
✅ Successfully read visitor count from KV
✅ Successfully updated visitor count in KV
```

**不应该再看到：**
```
❌ invalid URL
❌ KV connection failed
```

---

## 🔄 替代方案：选择 "Redis"

如果 "Upstash" 选项有问题，也可以选择：

**"Redis"** - "Serverless Redis"
- 这也提供 Redis/Key-Value 存储
- 可能使用不同的提供商
- 配置步骤类似

---

## ✅ 快速检查清单

- [ ] 选择了 "Upstash" 从 Marketplace Database Providers
- [ ] 创建了新的 Redis/KV 数据库
- [ ] 数据库已连接到 `matchwise-ai-app` 项目
- [ ] 确认 `KV_REST_API_URL` 和 `KV_REST_API_TOKEN` 已自动配置
- [ ] 删除了旧的 `REDIS_URL` 环境变量
- [ ] 重新部署了应用
- [ ] 验证了日志没有错误

---

## 💡 重要提示

1. **为什么选择 Upstash？**
   - `@vercel/kv` 底层使用 Upstash Redis
   - 你的旧数据库也是 Upstash
   - 选择 Upstash 确保兼容性

2. **为什么没有直接的 "KV" 选项？**
   - Vercel 已将 KV 移至 Marketplace
   - 现在通过第三方提供商（如 Upstash）提供

3. **环境变量会自动配置**
   - 创建数据库并连接项目后
   - Vercel 会自动添加必要的环境变量
   - 不需要手动配置

---

## 🔗 相关链接

- Vercel Storage: https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/storage
- 环境变量: https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables

---

**推荐操作**：选择 **"Upstash"** → 创建 Redis 数据库 → 连接到项目 → 重新部署
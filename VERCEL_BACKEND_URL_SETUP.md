# Vercel 后端 URL 配置检查清单

## ✅ 已完成的修复

### 代码修复

1. **修复了 `trial-status/route.ts`**
   - 从 `http://localhost:8000` 改为 `https://resume-matcher-backend-rrrw.onrender.com`

2. **修复了 `create-checkout-session/route.ts`**
   - 从 `http://localhost:8000` 改为 `https://resume-matcher-backend-rrrw.onrender.com`

3. **已提交并推送到 GitHub**
   - 提交：`c399137` - "fix: Update backend URL default values to use Render URL instead of localhost"

---

## 🔍 检查 Vercel 环境变量配置

### 步骤 1: 访问 Vercel 环境变量设置

1. **打开 Vercel Dashboard**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables

2. **查看环境变量列表**
   - 查找 `NEXT_PUBLIC_BACKEND_URL`

### 步骤 2: 检查环境变量

#### ✅ 如果环境变量已存在

确认以下信息：
- **Name**: `NEXT_PUBLIC_BACKEND_URL`
- **Value**: `https://resume-matcher-backend-rrrw.onrender.com`
- **Environment**: 应该包括：
  - ✅ Production
  - ✅ Preview
  - ✅ Development（可选）

#### ❌ 如果环境变量不存在

需要添加：

1. **点击 "Add Environment Variable" 按钮**

2. **填写信息：**
   ```
   Name: NEXT_PUBLIC_BACKEND_URL
   Value: https://resume-matcher-backend-rrrw.onrender.com
   ```

3. **选择环境：**
   - ✅ Production
   - ✅ Preview
   - ✅ Development（可选，用于本地开发）

4. **点击 "Save"**

5. **重新部署应用**
   - 环境变量更改后需要重新部署才能生效
   - 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments
   - 点击 "Redeploy" 或等待自动部署

---

## 📋 完整配置检查清单

### 代码配置 ✅

- [x] `page.tsx` - 使用正确的默认值
- [x] `api/user/use-trial/route.ts` - 使用正确的默认值
- [x] `api/user/status/route.ts` - 使用正确的默认值
- [x] `api/user/trial-status/route.ts` - **已修复** ✅
- [x] `api/create-checkout-session/route.ts` - **已修复** ✅

### Vercel 环境变量配置 ⚠️

- [ ] `NEXT_PUBLIC_BACKEND_URL` 环境变量已设置
- [ ] 值为 `https://resume-matcher-backend-rrrw.onrender.com`
- [ ] 在 Production 环境中设置
- [ ] 在 Preview 环境中设置（可选但推荐）

### 后端服务 ✅

- [x] Render 后端服务正常运行
- [x] Health check 可访问：https://resume-matcher-backend-rrrw.onrender.com/health
- [x] API 端点可访问：https://resume-matcher-backend-rrrw.onrender.com/api/compare

---

## 🎯 当前状态总结

### ✅ 已正确配置

1. **代码中的默认值** - 所有文件现在都使用 Render URL
2. **后端服务** - Render 服务正常运行
3. **主要功能** - API 调用应该能正常工作

### ⚠️ 需要确认

1. **Vercel 环境变量** - 需要检查是否已设置
   - 如果已设置：✅ 完美
   - 如果未设置：需要添加（见上面的步骤）

---

## 🚀 下一步操作

### 1. 检查 Vercel 环境变量

访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables

确认 `NEXT_PUBLIC_BACKEND_URL` 是否存在且值正确。

### 2. 如果环境变量不存在，添加它

按照上面的步骤添加环境变量。

### 3. 重新部署应用

- **自动部署**：如果已连接 GitHub，新提交会自动触发部署
- **手动部署**：在 Vercel Dashboard 中点击 "Redeploy"

### 4. 验证配置

部署完成后，测试应用功能：
- 提交简历和职位描述
- 检查 API 调用是否成功
- 查看浏览器控制台是否有错误

---

## 💡 重要提示

### 环境变量的优先级

1. **Vercel 环境变量**（最高优先级）
   - 如果设置了 `NEXT_PUBLIC_BACKEND_URL`，会使用这个值

2. **代码中的默认值**（备用）
   - 如果环境变量未设置，使用代码中的默认值
   - 现在所有默认值都是 Render URL ✅

### 为什么需要环境变量？

虽然代码中已有正确的默认值，但设置环境变量的好处：
- ✅ 可以轻松切换后端 URL（开发/生产）
- ✅ 不需要修改代码
- ✅ 更符合最佳实践
- ✅ 可以在不同环境中使用不同的 URL

---

## ✅ 配置完成后的验证

### 1. 检查环境变量

```bash
# 在 Vercel Dashboard 中查看
# 或使用 Vercel CLI
vercel env ls
```

### 2. 测试后端连接

访问应用并测试功能：
- 提交简历匹配请求
- 检查是否成功调用后端 API
- 查看浏览器 Network 标签，确认请求发送到正确的 URL

### 3. 检查部署日志

在 Vercel Dashboard 中查看部署日志：
- 确认构建成功
- 没有环境变量相关的错误

---

**总结**：代码已修复 ✅，现在需要检查 Vercel 环境变量配置。如果已设置，一切就绪；如果未设置，按照上面的步骤添加即可。
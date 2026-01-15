# 检查后端 URL 配置

## 🔍 当前状态

### ✅ 代码中的配置

后端 URL `https://resume-matcher-backend-rrrw.onrender.com` 在以下文件中使用：

1. **`resume-matcher-frontend/src/app/page.tsx`** ✅
   - 使用：`process.env.NEXT_PUBLIC_BACKEND_URL || 'https://resume-matcher-backend-rrrw.onrender.com'`
   - 状态：✅ 正确配置

2. **`resume-matcher-frontend/src/app/api/user/use-trial/route.ts`** ✅
   - 使用：`process.env.NEXT_PUBLIC_BACKEND_URL || 'https://resume-matcher-backend-rrrw.onrender.com'`
   - 状态：✅ 正确配置

3. **`resume-matcher-frontend/src/app/api/user/status/route.ts`** ✅
   - 使用：`process.env.NEXT_PUBLIC_BACKEND_URL || 'https://resume-matcher-backend-rrrw.onrender.com'`
   - 状态：✅ 正确配置

4. **`resume-matcher-frontend/src/app/api/user/trial-status/route.ts`** ⚠️
   - 使用：`process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'`
   - 状态：⚠️ **需要修复** - 默认值应该是 Render URL

5. **`resume-matcher-frontend/src/app/api/create-checkout-session/route.ts`** ⚠️
   - 使用：`process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'`
   - 状态：⚠️ **需要修复** - 默认值应该是 Render URL

---

## ⚠️ 需要修复的文件

有两个文件使用了错误的默认值 `http://localhost:8000`，应该改为 Render URL。

### 文件 1: `resume-matcher-frontend/src/app/api/user/trial-status/route.ts`

**当前代码：**
```typescript
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
```

**应该改为：**
```typescript
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://resume-matcher-backend-rrrw.onrender.com';
```

### 文件 2: `resume-matcher-frontend/src/app/api/create-checkout-session/route.ts`

**当前代码：**
```typescript
const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
```

**应该改为：**
```typescript
const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://resume-matcher-backend-rrrw.onrender.com';
```

---

## ✅ Vercel 环境变量配置检查

### 步骤 1: 检查 Vercel 环境变量

1. **访问 Vercel Dashboard**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables

2. **确认环境变量存在**
   - 查找：`NEXT_PUBLIC_BACKEND_URL`
   - 值应该是：`https://resume-matcher-backend-rrrw.onrender.com`

3. **检查环境范围**
   - 确保在以下环境中都设置了：
     - ✅ Production
     - ✅ Preview
     - ✅ Development（可选）

### 步骤 2: 如果环境变量不存在，添加它

1. **点击 "Add Environment Variable"**
2. **填写信息：**
   - **Name**: `NEXT_PUBLIC_BACKEND_URL`
   - **Value**: `https://resume-matcher-backend-rrrw.onrender.com`
   - **Environment**: 选择所有环境（Production, Preview, Development）
3. **点击 "Save"**

---

## 🔧 修复代码中的默认值

需要修复两个文件中的默认值，确保即使环境变量未设置，也使用正确的 Render URL。

---

## 📋 检查清单

### 代码配置
- [x] `page.tsx` - ✅ 正确
- [x] `api/user/use-trial/route.ts` - ✅ 正确
- [x] `api/user/status/route.ts` - ✅ 正确
- [ ] `api/user/trial-status/route.ts` - ⚠️ 需要修复
- [ ] `api/create-checkout-session/route.ts` - ⚠️ 需要修复

### Vercel 配置
- [ ] 环境变量 `NEXT_PUBLIC_BACKEND_URL` 已设置
- [ ] 值为 `https://resume-matcher-backend-rrrw.onrender.com`
- [ ] 在所有环境中都设置了（Production, Preview）

### 后端服务
- [x] Render 后端服务正常运行
- [x] Health check: https://resume-matcher-backend-rrrw.onrender.com/health

---

## 🎯 总结

### ✅ 已正确配置的部分

1. **大部分代码文件** - 使用正确的默认值
2. **后端服务** - Render 服务正常运行
3. **主要 API 调用** - 使用正确的 URL

### ⚠️ 需要修复的部分

1. **两个 API 路由文件** - 默认值需要更新
2. **Vercel 环境变量** - 需要确认已设置

### 🚀 下一步操作

1. **修复代码中的默认值**（2个文件）
2. **检查 Vercel 环境变量配置**
3. **重新部署前端应用**

---

**建议**：先检查 Vercel 环境变量，然后修复代码中的默认值，最后重新部署。
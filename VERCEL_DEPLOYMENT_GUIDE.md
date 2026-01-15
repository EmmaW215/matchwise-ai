# Vercel 部署指南 - MatchWise AI

## 📋 部署步骤

### 方法 1: 通过 Vercel Dashboard 连接 GitHub（推荐）

#### 步骤 1: 连接 GitHub 仓库

1. 访问 [Vercel Dashboard](https://vercel.com/emma-wangs-projects/matchwise-ai-app)
2. 点击 **"Settings"** → **"Git"**
3. 如果还没有连接，点击 **"Connect Git Repository"**
4. 选择 **GitHub** 作为 Git Provider
5. 搜索并选择仓库：`EmmaW215/matchwise-ai`
6. 点击 **"Import"**

#### 步骤 2: 配置项目设置

在 **"Settings"** → **"General"** 中配置：

**Root Directory:**
```
resume-matcher-frontend
```

**Framework Preset:**
```
Next.js
```

**Build Command:**
```
npm run build
```

**Output Directory:**
```
.next
```
（通常 Next.js 会自动检测，可以留空）

**Install Command:**
```
npm install
```

#### 步骤 3: 配置环境变量

在 **"Settings"** → **"Environment Variables"** 中添加：

```
NEXT_PUBLIC_BACKEND_URL=https://resume-matcher-backend-rrrw.onrender.com
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your_stripe_key
```

（根据你的实际环境变量添加）

#### 步骤 4: 触发部署

1. 如果已经连接了 GitHub，Vercel 会自动检测新的推送并开始部署
2. 或者手动触发：**"Deployments"** → **"Redeploy"**

---

### 方法 2: 使用 Vercel CLI（命令行）

#### 步骤 1: 安装 Vercel CLI

```bash
npm i -g vercel
```

#### 步骤 2: 登录 Vercel

```bash
vercel login
```

#### 步骤 3: 在项目目录中部署

```bash
cd resume-matcher-frontend
vercel --prod
```

#### 步骤 4: 配置项目

首次部署时，Vercel CLI 会询问：
- **Set up and deploy?** → `Y`
- **Which scope?** → 选择你的账户
- **Link to existing project?** → `Y` → 选择 `matchwise-ai-app`
- **What's your project's root directory?** → `./resume-matcher-frontend` 或直接回车（如果已经在目录中）
- **Override settings?** → `N`（除非需要修改）

---

## ⚙️ 重要配置说明

### Root Directory 配置

由于项目结构是：
```
matchwise-ai/
├── resume-matcher-frontend/  ← Next.js 项目在这里
└── resume-matcher-backend/
```

**必须在 Vercel 中设置 Root Directory 为 `resume-matcher-frontend`**

### 如何设置 Root Directory

1. 在 Vercel Dashboard 中，进入项目 **Settings**
2. 找到 **"Root Directory"** 设置
3. 点击 **"Edit"**
4. 输入：`resume-matcher-frontend`
5. 点击 **"Save"**

---

## 🔍 验证部署

### 检查部署状态

1. 访问 [Vercel Dashboard](https://vercel.com/emma-wangs-projects/matchwise-ai-app)
2. 查看 **"Deployments"** 标签页
3. 确认最新部署状态为 **"Ready"**

### 测试部署

访问部署后的 URL（通常在 Vercel Dashboard 的 **"Domains"** 部分显示）

测试功能：
- [ ] 页面正常加载
- [ ] 登录功能正常
- [ ] 简历上传功能正常
- [ ] API 调用正常

---

## 🐛 常见问题排查

### 问题 1: 构建失败 - "Cannot find module"

**原因**: Root Directory 配置错误

**解决方案**:
1. 检查 Root Directory 是否设置为 `resume-matcher-frontend`
2. 确认 `package.json` 在 `resume-matcher-frontend` 目录中

### 问题 2: 构建失败 - "Build command failed"

**原因**: 依赖安装或构建脚本问题

**解决方案**:
1. 检查 **Build Command** 是否为 `npm run build`
2. 查看构建日志中的具体错误信息
3. 确认所有依赖都在 `package.json` 中

### 问题 3: 环境变量未生效

**原因**: 环境变量未正确配置

**解决方案**:
1. 在 **Settings** → **Environment Variables** 中检查
2. 确保环境变量名称正确（注意 `NEXT_PUBLIC_` 前缀）
3. 重新部署以应用环境变量

### 问题 4: 自动部署未触发

**原因**: GitHub 连接问题或分支配置

**解决方案**:
1. 检查 **Settings** → **Git** 中的连接状态
2. 确认 **Production Branch** 设置为 `main`
3. 手动触发一次部署：**Deployments** → **Redeploy**

---

## 📝 部署后检查清单

- [ ] Root Directory 设置为 `resume-matcher-frontend`
- [ ] 环境变量已配置
- [ ] 构建成功完成
- [ ] 部署状态为 "Ready"
- [ ] 网站可以正常访问
- [ ] 所有功能测试通过
- [ ] SmartSuccess.AI 集成功能正常（iframe 嵌入测试）

---

## 🔗 相关链接

- [Vercel Dashboard](https://vercel.com/emma-wangs-projects/matchwise-ai-app)
- [GitHub Repository](https://github.com/EmmaW215/matchwise-ai)
- [Vercel Documentation](https://vercel.com/docs)

---

**提示**: 如果 Vercel 已经连接了 GitHub，推送代码后会自动触发部署。确保 Root Directory 配置正确即可。
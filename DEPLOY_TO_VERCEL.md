# 快速部署到 Vercel

## 🚀 方法 1: 通过 Vercel Dashboard（推荐）

### 步骤：

1. **访问 Vercel Dashboard**
   - 打开：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings

2. **连接 GitHub 仓库**
   - 如果显示 "Connect Git"，点击并选择：
     - Repository: `EmmaW215/matchwise-ai`
     - Root Directory: `resume-matcher-frontend` ⚠️ **重要！**
     - Framework Preset: `Next.js`

3. **配置 Root Directory**（如果已连接）
   - 进入 **Settings** → **General**
   - 找到 **Root Directory**
   - 设置为：`resume-matcher-frontend`
   - 点击 **Save**

4. **配置环境变量**
   - 进入 **Settings** → **Environment Variables**
   - 添加必要的环境变量（如果还没有）

5. **触发部署**
   - 如果已连接 GitHub，推送代码会自动触发部署
   - 或手动触发：**Deployments** → **Redeploy**

---

## 🛠️ 方法 2: 使用 Vercel CLI

### 在 resume-matcher-frontend 目录中运行：

```bash
cd resume-matcher-frontend
vercel --prod
```

---

## ⚠️ 重要配置

### Root Directory 必须设置为：`resume-matcher-frontend`

因为项目结构是：
```
matchwise-ai/                    ← GitHub 仓库根目录
└── resume-matcher-frontend/      ← Next.js 项目在这里
    ├── package.json
    ├── next.config.ts
    └── src/
```

---

## ✅ 验证部署

部署完成后，访问 Vercel 提供的 URL 测试功能。

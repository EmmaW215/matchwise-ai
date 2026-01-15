# 修复 Git 仓库和 Vercel CLI 问题

## 🔴 发现的问题

### 问题 1: 前端目录有独立的 Git 仓库

`resume-matcher-frontend` 目录有自己的 git 仓库，指向错误的仓库：
- ❌ 当前：`https://github.com/EmmaW215/resume-update-frontend.git`
- ✅ 应该是：使用项目根目录的仓库 `https://github.com/EmmaW215/matchwise-ai.git`

### 问题 2: Vercel CLI 路径错误

```
Error: The provided path ".../resume-matcher-frontend/resume-matcher-frontend" does not exist.
```

**原因：**
- Vercel 项目设置中的 Root Directory 已配置为 `resume-matcher-frontend`
- 在 `resume-matcher-frontend` 目录中运行 CLI 导致路径重复

## ✅ 解决方案

### 方案 1: 删除前端目录的独立 Git 仓库（推荐）

前端目录不应该有独立的 git 仓库，应该使用项目根目录的仓库。

#### 步骤：

1. **删除前端目录的 .git 文件夹**
   ```bash
   cd resume-matcher-frontend
   rm -rf .git
   ```

2. **确认使用项目根目录的仓库**
   ```bash
   cd ..
   git status
   # 应该显示整个项目的状态
   ```

3. **从项目根目录推送代码**
   ```bash
   git add .
   git commit -m "fix: Remove duplicate git repo in frontend directory"
   git push origin main
   ```

### 方案 2: 使用 GitHub 自动部署（最简单）

**不需要使用 CLI！**

1. **从项目根目录推送代码**
   ```bash
   cd /Users/emmawang/Library/Mobile\ Documents/com~apple~CloudDocs/Emma\ My\ Product/AI_Projects/h_MatchWise_AI
   git add .
   git commit -m "fix: Update project"
   git push origin main
   ```

2. **Vercel 会自动部署**
   - 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments
   - 应该看到新的部署

### 方案 3: 如果必须使用 CLI

从**项目根目录**运行：

```bash
# 从项目根目录
cd /Users/emmawang/Library/Mobile\ Documents/com~apple~CloudDocs/Emma\ My\ Product/AI_Projects/h_MatchWise_AI

# 使用 --cwd 参数
vercel --prod --cwd resume-matcher-frontend
```

---

## 🎯 推荐操作步骤

### 步骤 1: 删除前端目录的独立 Git 仓库

```bash
cd resume-matcher-frontend
rm -rf .git
cd ..
```

### 步骤 2: 从项目根目录推送代码

```bash
# 确保在项目根目录
cd /Users/emmawang/Library/Mobile\ Documents/com~apple~CloudDocs/Emma\ My\ Product/AI_Projects/h_MatchWise_AI

# 检查状态
git status

# 添加所有更改
git add .

# 提交
git commit -m "fix: Remove duplicate git repo and update project"

# 推送到正确的仓库
git push origin main
```

### 步骤 3: 检查 Vercel 自动部署

1. **访问 Vercel Dashboard**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments

2. **确认新部署**
   - 应该看到基于最新提交的新部署
   - 等待部署完成

---

## 🔍 为什么会出现这个问题？

1. **前端目录有独立的 Git 仓库**
   - 可能是之前单独管理前端项目时创建的
   - 现在应该使用项目根目录的统一仓库

2. **Vercel CLI 路径问题**
   - Root Directory 配置为 `resume-matcher-frontend`
   - 在子目录中运行 CLI 导致路径重复

---

## ✅ 修复后的状态

修复后：
- ✅ 只有一个 Git 仓库（在项目根目录）
- ✅ 所有代码从项目根目录推送
- ✅ Vercel 自动检测 GitHub 推送并部署
- ✅ 不需要使用 CLI

---

**推荐**：删除前端目录的 `.git` 文件夹，然后从项目根目录推送代码，让 Vercel 自动部署。
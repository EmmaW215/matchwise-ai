# Vercel 部署错误排查指南

## 🔍 常见部署错误及解决方案

### 错误 1: Module not found / Cannot find module

**错误信息示例：**
```
Module not found: Can't resolve '@/firebase'
Error: Cannot find module '../../firebase'
```

**原因：**
- 导入路径错误
- 文件不存在

**解决方案：**
1. 检查 `src/firebase.ts` 文件是否存在
2. 确认导入路径正确：
   - 从 `src/app/hooks/` 导入：`../../firebase`
   - 从 `src/app/components/` 导入：`../../firebase`
   - 从 `src/app/page.tsx` 导入：`../firebase`

### 错误 2: TypeScript 类型错误

**错误信息示例：**
```
Type error: Property 'xxx' does not exist on type 'xxx'
```

**原因：**
- TypeScript 类型定义问题
- 缺少类型声明

**解决方案：**
1. 检查 `tsconfig.json` 配置
2. 确认所有类型定义正确
3. 运行 `npm run build` 本地测试

### 错误 3: 环境变量未定义

**错误信息示例：**
```
NEXT_PUBLIC_BACKEND_URL is not defined
```

**原因：**
- 环境变量未在 Vercel 中配置

**解决方案：**
1. 访问 Vercel Dashboard → Settings → Environment Variables
2. 添加缺失的环境变量
3. 重新部署

### 错误 4: 构建超时

**错误信息示例：**
```
Build exceeded maximum build time
```

**原因：**
- 构建时间过长
- 依赖安装慢

**解决方案：**
1. 检查 `package.json` 中的依赖
2. 移除不必要的依赖
3. 优化构建配置

### 错误 5: ESLint 错误

**错误信息示例：**
```
ESLint: 'xxx' is assigned a value but never used
```

**原因：**
- 代码中有未使用的变量
- ESLint 规则严格

**解决方案：**
1. 移除未使用的变量
2. 或添加 `eslint-disable` 注释

---

## 🛠️ 快速修复步骤

### 步骤 1: 查看完整错误日志

1. 访问 Vercel Dashboard
2. 点击失败的部署
3. 查看 "Build Logs"
4. 复制完整的错误信息

### 步骤 2: 本地测试构建

```bash
cd resume-matcher-frontend
npm install
npm run build
```

如果本地构建失败，错误信息会显示具体问题。

### 步骤 3: 检查常见问题

- [ ] 所有导入路径正确
- [ ] 所有文件存在
- [ ] TypeScript 类型正确
- [ ] 环境变量已配置
- [ ] 依赖已安装

### 步骤 4: 修复并重新部署

1. 修复发现的问题
2. 提交更改到 Git
3. 推送到 GitHub
4. Vercel 会自动重新部署

---

## 📋 请提供以下信息以便诊断

1. **完整的错误信息**（从 Vercel 构建日志中复制）
2. **错误发生的阶段**（安装依赖 / 构建 / 部署）
3. **具体的错误行号**（如果有）
4. **本地构建是否成功**

---

## 🔗 有用的链接

- Vercel 构建日志：https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments
- Vercel 文档：https://vercel.com/docs
- Next.js 部署文档：https://nextjs.org/docs/deployment

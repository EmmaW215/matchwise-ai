# 修复 CORS 错误 - 新 Vercel 项目

## 🔴 问题

**错误信息：**
```
Access to fetch at 'https://resume-matcher-backend-rrrw.onrender.com/api/compare' 
from origin 'https://matchwise-ai2026.vercel.app' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**原因：**
- 新 Vercel 项目部署在：`https://matchwise-ai2026.vercel.app`
- 后端 CORS 配置中只包含：`https://matchwise-ai.vercel.app`
- 新域名不在允许列表中

---

## ✅ 解决方案

有两种方法修复这个问题：

### 方法 1: 在 Render 环境变量中添加（推荐，最快）

这是最简单的方法，不需要修改代码。

#### 步骤：

1. **访问 Render Dashboard**
   - https://dashboard.render.com

2. **选择后端服务**
   - 找到 `resume-matcher-backend` 服务

3. **进入环境变量设置**
   - 点击 "Environment" 标签页

4. **添加或更新 `ALLOWED_ORIGINS` 环境变量**
   - 如果已存在，点击编辑
   - 如果不存在，点击 "Add Environment Variable"
   - **Name**: `ALLOWED_ORIGINS`
   - **Value**: `https://matchwise-ai2026.vercel.app`
   - 如果已有其他域名，用逗号分隔：
     ```
     https://matchwise-ai2026.vercel.app,https://matchwise-ai.vercel.app
     ```

5. **保存并重新部署**
   - 点击 "Save Changes"
   - Render 会自动重新部署服务
   - 等待部署完成（通常 2-5 分钟）

---

### 方法 2: 更新后端代码（永久解决方案）

更新后端代码，将新域名添加到默认允许列表。

#### 步骤：

1. **更新 `resume-matcher-backend/main.py`**

   找到 CORS 配置部分（大约第 158-165 行）：

   **当前代码：**
   ```python
   allowed_origins = [
       "https://matchwise-ai.vercel.app",
       "http://localhost:3000",
       "http://localhost:3001",
       "http://127.0.0.1:3000",
       "http://192.168.86.47:3000"
   ]
   ```

   **更新为：**
   ```python
   allowed_origins = [
       "https://matchwise-ai.vercel.app",
       "https://matchwise-ai2026.vercel.app",  # 新增
       "https://*.vercel.app",  # 允许所有 Vercel 子域名（可选）
       "http://localhost:3000",
       "http://localhost:3001",
       "http://127.0.0.1:3000",
       "http://192.168.86.47:3000"
   ]
   ```

   **注意**：FastAPI 的 CORS 不支持通配符 `*.vercel.app`，所以需要明确列出每个域名。

2. **提交并推送代码**
   ```bash
   cd resume-matcher-backend
   git add main.py
   git commit -m "fix: Add new Vercel project domain to CORS allowed origins"
   git push origin main
   ```

3. **等待 Render 自动部署**
   - Render 会自动检测 GitHub 推送并重新部署

---

## 🎯 推荐操作

**立即执行方法 1**（最快）：
1. 在 Render Dashboard 中添加 `ALLOWED_ORIGINS` 环境变量
2. 值为：`https://matchwise-ai2026.vercel.app`
3. 等待重新部署完成

**然后执行方法 2**（永久修复）：
1. 更新后端代码
2. 提交并推送
3. 这样以后就不需要每次都在环境变量中添加新域名了

---

## 🔍 验证修复

部署完成后，测试：

1. **访问前端应用**
   - https://matchwise-ai2026.vercel.app

2. **尝试生成比较**
   - 上传简历和职位描述
   - 点击 "Generate Comparison"
   - 应该不再出现 CORS 错误

3. **检查浏览器控制台**
   - 不应该再看到 CORS 错误
   - API 请求应该成功

---

## 📋 当前后端 CORS 配置

后端代码支持通过环境变量添加额外的允许域名：

```python
# 默认允许的域名
allowed_origins = [
    "https://matchwise-ai.vercel.app",
    "http://localhost:3000",
    # ...
]

# 从环境变量读取额外域名
if os.getenv("ALLOWED_ORIGINS"):
    additional_origins = os.getenv("ALLOWED_ORIGINS")
    if additional_origins:
        allowed_origins.extend(additional_origins.split(","))
```

所以可以通过 `ALLOWED_ORIGINS` 环境变量快速添加新域名，无需修改代码。

---

## ⚠️ 重要提示

1. **环境变量格式**
   - 多个域名用逗号分隔
   - 不要有空格（或确保格式正确）
   - 示例：`https://domain1.com,https://domain2.com`

2. **重新部署**
   - 修改环境变量后，Render 会自动重新部署
   - 等待部署完成后再测试

3. **多个 Vercel 项目**
   - 如果以后创建更多 Vercel 项目，记得在 `ALLOWED_ORIGINS` 中添加新域名
   - 或者更新代码，添加所有域名到默认列表

---

**推荐**：立即在 Render 环境变量中添加 `ALLOWED_ORIGINS`，这是最快的解决方法！
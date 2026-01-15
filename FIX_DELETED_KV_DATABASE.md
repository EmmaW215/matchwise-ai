# 修复已删除的 KV 数据库

## 🔴 问题诊断

你的 `matchwise-kv` 数据库因为 14 天不活跃被自动删除了（Free 计划限制）。

**当前状态：**
- ❌ 数据库状态：`DELETED` / `Archived due to inactivity`
- ❌ 集成状态：`Uninstalled`
- ❌ "Connect Project" 按钮：灰色不可用
- ❌ 恢复时没有目标数据库可选

## ✅ 解决方案：创建新的 Vercel KV 数据库

由于访客计数器数据可以从头开始，最简单的方法是创建一个新的数据库。

### 方法 1: 在 Vercel Dashboard 中创建新数据库（推荐）

#### 步骤 1: 创建新的 KV 数据库

1. **访问 Vercel Storage**
   - 打开：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/storage

2. **创建新数据库**
   - 点击 **"Create Database"** 按钮（右上角黑色按钮）
   - 选择 **"KV"** (Key-Value)
   - 输入数据库名称，例如：`matchwise-kv-new` 或 `matchwise-kv`
   - 选择计划：**Free**（如果可用）
   - 点击 **"Create"**

3. **等待创建完成**
   - Vercel 会自动创建数据库
   - 自动配置环境变量

#### 步骤 2: 连接数据库到项目

1. **连接项目**
   - 创建完成后，会看到 "Connect Project" 选项
   - 选择项目：`matchwise-ai-app`
   - 点击 **"Connect"**

2. **确认环境变量自动配置**
   - Vercel 会自动添加以下环境变量到项目：
     - `KV_REST_API_URL`
     - `KV_REST_API_TOKEN`
     - `KV_URL`
   - 这些变量会自动在部署时可用

#### 步骤 3: 删除旧的环境变量（如果有）

1. **访问环境变量设置**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables

2. **删除旧的 REDIS_URL**
   - 如果存在 `REDIS_URL` 环境变量，删除它
   - Vercel KV 不需要这个变量

3. **确认新的环境变量**
   - 应该看到 `KV_REST_API_URL` 和 `KV_REST_API_TOKEN`
   - 这些是 Vercel 自动添加的

#### 步骤 4: 重新部署

1. **触发重新部署**
   - 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments
   - 点击最新部署的 **"..."** 菜单
   - 选择 **"Redeploy"**

2. **验证部署**
   - 等待部署完成
   - 检查日志，应该不再有 KV 连接错误

---

### 方法 2: 如果需要恢复旧数据

如果你需要恢复旧的访客计数数据：

#### 步骤 1: 创建新的目标数据库

1. 在 Vercel Dashboard 中创建新的 KV 数据库（如方法 1 的步骤 1-2）

#### 步骤 2: 在 Upstash 控制台恢复

1. **访问 Upstash 控制台**
   - 点击 "Open in Upstash" 按钮
   - 或访问：https://console.upstash.com/

2. **找到备份**
   - 在 "INACTIVE" 部分找到 `matchwise-kv`
   - 点击 **"Restore"** 按钮

3. **选择目标数据库**
   - 在 "Migrate Database" 对话框中
   - **"From"**: 选择备份（`matchwise-kv-before-deletion backup-2025-10-15`）
   - **"To"**: 选择新创建的数据库（现在应该可以选择了）
   - 勾选确认框
   - 点击 **"Start Migration"**

4. **等待恢复完成**
   - 恢复过程可能需要几分钟
   - 完成后，数据会迁移到新数据库

---

## 🔧 快速修复步骤（推荐）

如果你不需要恢复旧数据，这是最快的方案：

### ✅ 完整步骤：

1. **创建新数据库**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/storage
   - 点击 "Create Database" → 选择 "KV" → 创建

2. **连接项目**
   - 创建后，点击 "Connect Project"
   - 选择 `matchwise-ai-app`

3. **删除旧的 REDIS_URL**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables
   - 删除 `REDIS_URL`（如果存在）

4. **重新部署**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments
   - 点击 "Redeploy"

5. **验证**
   - 检查部署日志
   - 测试 `/api/visitor-stats` 端点

---

## 📋 检查清单

- [ ] 创建了新的 Vercel KV 数据库
- [ ] 数据库已连接到 `matchwise-ai-app` 项目
- [ ] 确认 Vercel 自动配置了 `KV_REST_API_URL` 和 `KV_REST_API_TOKEN`
- [ ] 删除了旧的 `REDIS_URL` 环境变量（如果存在）
- [ ] 重新部署了应用
- [ ] 验证了部署日志没有错误
- [ ] 测试了访客计数器功能

---

## 🎯 预期结果

部署成功后：

1. **日志中应该看到：**
   ```
   ✅ Successfully read visitor count from KV
   ✅ Successfully updated visitor count in KV
   ```

2. **不应该再看到：**
   ```
   ❌ invalid URL
   ❌ KV connection failed
   ```

3. **访客计数器功能：**
   - 页面加载时显示访客数
   - 每次访问自动增加计数
   - 数据保存在新的 KV 数据库中

---

## 🔗 相关链接

- **Vercel Storage**: https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/storage
- **环境变量**: https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables
- **部署历史**: https://vercel.com/emma-wangs-projects/matchwise-ai-app/deployments

---

## 💡 重要提示

1. **访客计数器会重置**：创建新数据库后，访客计数会从 0 开始（或代码中的初始值 116）
2. **不需要恢复旧数据**：如果访客计数不重要，直接创建新数据库即可
3. **Vercel KV 自动配置**：创建数据库后，Vercel 会自动配置所有必要的环境变量
4. **Free 计划限制**：Free 计划的数据库在 14 天不活跃后会被删除，这是正常行为

---

**推荐操作**：直接创建新数据库，不需要恢复旧数据。访客计数器会从初始值重新开始计数。
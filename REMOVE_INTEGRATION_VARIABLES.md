# 删除集成管理的环境变量

## 🔴 问题

前5个环境变量（`KV_URL`, `KV_REST_API_READ_ONLY_TOKEN`, `REDIS_URL`, `KV_REST_API_TOKEN`, `KV_REST_API_URL`）的 "Remove" 按钮是灰色的，无法删除。

## 🔍 原因

这些变量是由 **Vercel 集成（Integration）** 自动管理的，不能直接从环境变量页面删除。它们与数据库连接绑定。

## ✅ 解决方案

### 方法 1: 断开数据库连接（推荐）

#### 步骤 1: 访问 Storage 页面

1. **打开 Storage 设置**
   - 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/storage

2. **找到旧的数据库**
   - 找到 `matchwise-kv` 或任何已连接的旧数据库
   - 应该显示为 "Archived" 或 "Deleted" 状态

#### 步骤 2: 断开连接

1. **点击数据库名称** 或 **"..."** 菜单
2. **选择 "Disconnect"** 或 **"Uninstall"**
   - 这会断开数据库与项目的连接
   - 自动删除由集成管理的环境变量

3. **确认断开**
   - 确认操作
   - 等待几秒钟让 Vercel 同步

#### 步骤 3: 验证变量已删除

1. **返回环境变量页面**
   - https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables

2. **确认变量已消失**
   - `KV_URL` 应该不再存在
   - `REDIS_URL` 应该不再存在
   - `KV_REST_API_*` 变量应该不再存在

#### 步骤 4: 连接新数据库

1. **返回 Storage 页面**
2. **找到 `matchwise-kv-new` 数据库**
3. **点击 "Connect Project"**
4. **现在应该可以成功连接**（没有冲突）

---

### 方法 2: 通过 "Manage Connection" 断开

#### 步骤 1: 使用 "Manage Connection" 选项

1. **在环境变量页面**
   - 找到 `KV_REST_API_TOKEN` 或任何带红色图标的变量
   - 点击 **"..."** 菜单
   - 选择 **"Manage Connection"**

2. **这会打开集成管理页面**
   - 显示数据库连接详情
   - 应该有 "Disconnect" 或 "Uninstall" 选项

3. **断开连接**
   - 点击 "Disconnect" 或 "Uninstall"
   - 确认操作

---

### 方法 3: 删除整个数据库（如果不再需要）

如果旧数据库完全不需要了：

1. **访问 Storage 页面**
2. **找到旧数据库**（`matchwise-kv`）
3. **点击 "..."** 菜单
4. **选择 "Delete"** 或 **"Remove"**
5. **确认删除**
   - 这会删除数据库并断开所有连接
   - 自动清理所有相关环境变量

---

## 📋 完整操作步骤（推荐流程）

### 步骤 1: 断开旧数据库连接

1. 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/storage
2. 找到旧的 `matchwise-kv` 数据库（Archived/Deleted 状态）
3. 点击数据库名称或 "..." 菜单
4. 选择 **"Disconnect"** 或 **"Uninstall"**
5. 确认断开

### 步骤 2: 验证变量已删除

1. 访问：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables
2. 确认前5个变量已消失
3. 如果还在，等待 1-2 分钟让 Vercel 同步

### 步骤 3: 连接新数据库

1. 返回 Storage 页面
2. 找到 `matchwise-kv-new` 数据库
3. 点击 **"Connect Project"**
4. 在配置对话框中：
   - 选择需要的环境（Development, Preview, Production）
   - Custom Prefix 留空
   - 点击 **"Connect"**
5. 现在应该可以成功连接

### 步骤 4: 验证新变量

1. 返回环境变量页面
2. 确认新的变量已自动创建：
   - ✅ `KV_REST_API_URL` - 应该以 `https://` 开头
   - ✅ `KV_REST_API_TOKEN` - API 令牌
3. 确认格式正确

### 步骤 5: 重新部署

1. 访问部署页面
2. 触发重新部署
3. 验证日志没有错误

---

## 🔍 如何识别集成管理的变量

**特征：**
- ✅ 变量名旁边有**红色图标**（停止标志或链接图标）
- ✅ "Remove" 按钮是**灰色的**，带锁图标
- ✅ 菜单中有 **"Manage Connection"** 选项
- ✅ 显示 "Added" 日期而不是 "Updated"

**普通变量：**
- ❌ 没有红色图标
- ✅ "Remove" 按钮可用
- ❌ 没有 "Manage Connection" 选项

---

## 💡 重要提示

1. **断开连接会自动删除变量**
   - 不需要手动删除
   - Vercel 会自动清理

2. **等待同步**
   - 断开连接后，等待 1-2 分钟
   - 让 Vercel 同步更改

3. **检查所有环境**
   - 确保在所有环境中都断开了连接

4. **新数据库会自动创建变量**
   - 连接新数据库后
   - Vercel 会自动创建新的环境变量

---

## 🔗 相关链接

- Storage 设置：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/storage
- 环境变量：https://vercel.com/emma-wangs-projects/matchwise-ai-app/settings/environment-variables
- 集成管理：通过 "Manage Connection" 访问

---

**推荐操作**：断开旧数据库连接 → 验证变量已删除 → 连接新数据库 → 重新部署
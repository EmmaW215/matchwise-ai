# SmartSuccess.AI 集成快速开始

## 🎯 两边需要做的事情

### MatchWise AI 端（已完成 ✅）

所有代码已经实现完成，只需要：

1. **部署到生产环境**
   ```bash
   cd resume-matcher-frontend
   npm run build
   # 部署到 Vercel 或其他平台
   ```

2. **获取生产环境 URL**
   - 例如：`https://matchwise-ai.vercel.app`
   - 将这个 URL 提供给 SmartSuccess.AI 团队

3. **确认域名配置**（如果需要）
   - 如果 SmartSuccess.AI 使用不同的域名，需要更新：
     - `resume-matcher-frontend/src/app/hooks/useParentMessage.ts` 中的 `allowedOrigins`
     - `resume-matcher-frontend/next.config.ts` 中的 `frame-ancestors`

---

### SmartSuccess.AI 端（需要实现）

#### 1. 在 Home 页面添加 iframe

```tsx
// 替换为 MatchWise AI 的实际生产环境 URL
const MATCHWISE_URL = 'https://matchwise-ai.vercel.app';

<iframe
  src={MATCHWISE_URL}
  style={{ width: '100%', height: '100vh', border: 'none' }}
/>
```

#### 2. 添加消息监听器

```tsx
useEffect(() => {
  const handleMessage = (event: MessageEvent) => {
    // 安全检查
    if (event.origin !== MATCHWISE_URL) return;
    
    // 处理登录状态
    if (event.data.type === 'loginStatus') {
      // 更新登录状态
    }
    if (event.data.type === 'loginSuccess') {
      // 处理登录成功
    }
  };
  
  window.addEventListener('message', handleMessage);
  return () => window.removeEventListener('message', handleMessage);
}, []);
```

#### 3. 发送消息到 MatchWise AI

```tsx
// 隐藏访客计数器
iframeRef.current?.contentWindow?.postMessage(
  { action: 'hideVisitorCounter' },
  MATCHWISE_URL
);

// 查询登录状态
iframeRef.current?.contentWindow?.postMessage(
  { action: 'getLoginStatus' },
  MATCHWISE_URL
);

// 显示登录弹窗
iframeRef.current?.contentWindow?.postMessage(
  { action: 'showLoginModal', message: 'Please sign in' },
  MATCHWISE_URL
);
```

---

## 📋 完整代码示例

查看 `SMARTSUCCESS_INTEGRATION_GUIDE.md` 获取完整的代码示例和详细说明。

---

## ✅ 测试清单

- [ ] iframe 能正常加载
- [ ] 消息通信正常
- [ ] 登录状态同步
- [ ] 访客计数器隐藏
- [ ] 登录弹窗显示

---

## 🔗 相关文档

- 详细指南：`SMARTSUCCESS_INTEGRATION_GUIDE.md`
- 需求文档：`MatchWise_AI_Integration_Requirements.md`
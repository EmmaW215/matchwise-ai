import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,

  // 允许被 SmartSuccess.AI 嵌入
  // 使用 Content-Security-Policy 的 frame-ancestors 指令
  // 注意：X-Frame-Options 已被废弃，不应该使用
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Content-Security-Policy',
            // 允许 SmartSuccess.AI 和所有 Vercel 域名嵌入
            // 'self' - 允许同源嵌入
            // https://smartsuccess-ai.vercel.app - SmartSuccess.AI Vercel 部署
            // https://*.vercel.app - 所有 Vercel 子域名（包括预览部署）
            // http://localhost:* - 允许本地开发环境（所有端口）
            // http://127.0.0.1:* - 允许本地开发环境（IP 地址，所有端口）
            value: "frame-ancestors 'self' https://smartsuccess-ai.vercel.app https://*.vercel.app http://localhost:* http://127.0.0.1:*;",
          },
        ],
      },
    ];
  },

  // 允许开发环境的跨域请求
  allowedDevOrigins: [
    '192.168.86.46',
    'localhost',
    '127.0.0.1',
  ],
};

export default nextConfig;

import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,

  // 允许被 SmartSuccess.AI 嵌入
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          // 使用 Content-Security-Policy 的 frame-ancestors 指令
          {
            key: 'Content-Security-Policy',
            value: "frame-ancestors 'self' https://smartsuccess-ai.vercel.app https://*.vercel.app;",
          },
        ],
      },
    ];
  },
};

export default nextConfig;

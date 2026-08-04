import type { NextConfig } from "next";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "https://zus-call-fantastic-preference.trycloudflare.com";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${BACKEND_URL}/api/:path*`,
      },
      {
        source: "/projects/:path*",
        destination: `${BACKEND_URL}/api/projects/:path*`,
      },
      {
        source: "/auth/:path*",
        destination: `${BACKEND_URL}/api/auth/:path*`,
      },
    ];
  },
};

export default nextConfig;

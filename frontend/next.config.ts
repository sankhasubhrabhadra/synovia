import type { NextConfig } from "next";

const ACTIVE_TUNNEL_URL = "https://tours-farms-namely-finger.trycloudflare.com";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${ACTIVE_TUNNEL_URL}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;

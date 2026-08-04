import type { NextConfig } from "next";

const BACKEND_TUNNEL_URL = process.env.NEXT_PUBLIC_API_URL || "https://owned-brighton-guidelines-qualify.trycloudflare.com";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${BACKEND_TUNNEL_URL}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;

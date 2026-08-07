import type { NextConfig } from "next";

const ACTIVE_TUNNEL_URL = "https://large-apply-occurring-bench.trycloudflare.com";

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

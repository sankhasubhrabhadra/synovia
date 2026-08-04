import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // No rewrites — frontend calls the backend directly via CLOUDFLARE_TUNNEL_URL
};

export default nextConfig;

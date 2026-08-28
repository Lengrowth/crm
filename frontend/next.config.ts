import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.SAAS_BACKEND_INTERNAL_URL ?? "http://127.0.0.1:8001"}/:path*`,
      },
    ];
  },
};

export default nextConfig;

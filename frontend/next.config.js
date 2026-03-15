/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/memoryos/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8765'}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Static export: the FastAPI backend serves the generated files from
  // frontend/out so the whole IDE ships in a single container
  output: 'export',
};

export default nextConfig;

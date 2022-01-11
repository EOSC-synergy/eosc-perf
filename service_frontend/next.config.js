let withBundleAnalyzer = undefined;
try {
    withBundleAnalyzer = require('@next/bundle-analyzer')({
        enabled: process.env.ANALYZE === 'true'
    });
} catch (e) {
    console.log('No @next/bundle-analyzer, assuming production');
    withBundleAnalyzer = () => {
    };
}

/** @type {import('next').NextConfig} */
module.exports = {
    reactStrictMode: true,
    async redirects() {
        return [
            {
                source: '/',
                destination: '/search/result',
                permanent: true
            }
        ];
    },
    ...withBundleAnalyzer({})
};

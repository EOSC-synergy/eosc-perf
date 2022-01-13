import 'prismjs/themes/prism-dark.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import type { AppProps } from 'next/app';
import { QueryClientWrapper } from 'components/queryClientWrapper';
import { AuthProvider, AuthProviderProps } from 'react-oidc-context';
import { UserContextWrapper } from 'components/userContextWrapper';
import { NavHeader } from 'components/navHeader';
import { Footer } from 'components/footer';
import { useRouter } from 'next/router';
import { SSRProvider } from 'react-bootstrap';

const oidcConfig: AuthProviderProps = {
    authority:
        process.env.NODE_ENV === 'development'
            ? 'https://aai-dev.egi.eu/oidc/'
            : 'https://aai.egi.eu/oidc/',
    client_id: process.env.NEXT_PUBLIC_OIDC_CLIENT_ID ?? 'eosc-performance',
    redirect_uri: 'https://' + process.env.NEXT_PUBLIC_OIDC_REDIRECT_HOST + '/oidc-redirect',
    scope: 'openid email profile eduperson_entitlement offline_access',
    //autoSignIn: false,
    response_type: 'code',
};

function MyApp({ Component, pageProps }: AppProps) {
    const router = useRouter();

    return (
        <SSRProvider>
            <QueryClientWrapper>
                <AuthProvider
                    {...oidcConfig}
                    onSigninCallback={() => {
                        router.push('/');
                    }}
                >
                    <UserContextWrapper>
                        <NavHeader />
                        <Component {...pageProps} />
                        <Footer />
                    </UserContextWrapper>
                </AuthProvider>
            </QueryClientWrapper>
        </SSRProvider>
    );
}

export default MyApp;

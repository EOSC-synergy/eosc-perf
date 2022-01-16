import React, { ReactElement } from 'react';
import Head from 'next/head';

/**
 * Dummy page for oidc-redirect route.
 *
 * Once react-oidc-context is done, the user is redirected to the home page.
 *
 * @returns {React.ReactElement}
 * @constructor
 */
function OidcRedirect(): ReactElement {
    return (
        <>
            <Head>
                <title>Redirecting</title>
            </Head>
            Logging you in...
        </>
    );
}

export default OidcRedirect;

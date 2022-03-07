import React, { ReactElement } from 'react';
import Head from 'next/head';
import { Container } from 'react-bootstrap';

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
            <Container>Logging you in...</Container>
        </>
    );
}

export default OidcRedirect;

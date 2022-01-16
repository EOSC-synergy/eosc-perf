import React, { ReactElement } from 'react';
import { Container } from 'react-bootstrap';
import Head from 'next/head';
import { TermsOfService } from '../components/termsOfService';

/**
 * Page containing our terms of service / acceptable use policy.
 *
 * @returns {React.ReactElement}
 * @constructor
 */
function TermsOfServicePage(): ReactElement {
    return (
        <>
            <Head>
                <title>Acceptable Use Policy</title>
            </Head>
            <Container>
                <TermsOfService />
            </Container>
        </>
    );
}

export default TermsOfServicePage;

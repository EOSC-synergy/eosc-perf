import React, { ReactElement } from 'react';
import { Container } from 'react-bootstrap';
import { PageBase } from '../pageBase';

function TermsOfService(): ReactElement {
    return (
        <Container>
            <h1>Hello world!</h1>
        </Container>
    );
}

const TermsOfServiceModule: PageBase = {
    path: '/terms-of-service',
    element: TermsOfService,
    name: 'TermsOfService',
    displayName: 'Terms of Service',
};

export default TermsOfServiceModule;

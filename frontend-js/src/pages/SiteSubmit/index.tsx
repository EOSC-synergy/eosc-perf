import React, { ReactElement, useState } from 'react';
import { Card, Container, Toast } from 'react-bootstrap';
import { PageBase } from '../pageBase';
import { SiteSubmitForm } from 'components/forms/siteSubmitForm';

function SiteSubmission(): ReactElement {
    const [showSuccessToast, setShowSuccessToast] = useState(false);

    return (
        <Container>
            <h1>Add Site</h1>
            <Card className="mb-2">
                <Card.Body>
                    <SiteSubmitForm
                        onSuccess={() => {
                            setShowSuccessToast(true);
                        }}
                        onError={() => undefined}
                    />
                </Card.Body>
            </Card>
            <Toast
                show={showSuccessToast}
                onClose={() => setShowSuccessToast(false)}
                delay={5000}
                autohide
            >
                <Toast.Header>
                    <strong className="me-auto">eosc-perf</strong>
                </Toast.Header>
                <Toast.Body>Submission successful.</Toast.Body>
            </Toast>
        </Container>
    );
}

const SiteSubmissionModule: PageBase = {
    path: '/site-submission',
    element: SiteSubmission,
    name: 'SiteSubmission',
    displayName: 'Site',
};

export default SiteSubmissionModule;

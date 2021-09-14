import React, { useState } from 'react';
import { Container, Toast } from 'react-bootstrap';
import { PageBase } from '../pageBase';
import { SiteSubmitForm } from 'components/forms/siteSubmitForm';

function SiteSubmission() {
    const [showSuccessToast, setShowSuccessToast] = useState(false);

    return (
        <Container>
            <h1>Add Site</h1>
            <SiteSubmitForm
                onSuccess={() => {
                    setShowSuccessToast(true);
                }}
                onError={() => {}}
            />
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

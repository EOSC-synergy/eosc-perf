import React, { useState } from 'react';
import { Card, Container, Toast } from 'react-bootstrap';
import { Result } from 'api';
import { PageBase } from '../pageBase';
import { ResultSubmitForm } from 'components/forms/resultSubmitForm';

function ResultSubmission() {
    const [showSuccessToast, setShowSuccessToast] = useState(false);

    return (
        <Container>
            <h1>Upload Result</h1>
            <Card className="mb-2">
                <Card.Body>
                    <ResultSubmitForm
                        onSuccess={() => {
                            setShowSuccessToast(true);
                        }}
                        onError={() => {}}
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

const ResultSubmissionModule: PageBase = {
    path: '/result-submission',
    element: ResultSubmission,
    name: 'ResultSubmission',
    displayName: 'Result',
};

export default ResultSubmissionModule;

import React, { ReactElement, useState } from 'react';
import { Card, Container, Toast, ToastContainer } from 'react-bootstrap';
import { Page } from 'pages/page';
import { BenchmarkSubmitForm } from 'components/forms/benchmarkSubmitForm';

function BenchmarkSubmission(): ReactElement {
    const [showSuccessToast, setShowSuccessToast] = useState(false);

    return (
        <Container>
            <h1>Add Benchmark</h1>
            <Card className="mb-2">
                <Card.Body>
                    <BenchmarkSubmitForm
                        onSuccess={() => {
                            setShowSuccessToast(true);
                        }}
                        onError={() => undefined}
                    />
                </Card.Body>
            </Card>
            <ToastContainer position="middle-center">
                <Toast
                    show={showSuccessToast}
                    onClose={() => setShowSuccessToast(false)}
                    delay={4000}
                    autohide
                >
                    <Toast.Header>
                        <strong className="me-auto">eosc-perf</strong>
                    </Toast.Header>
                    <Toast.Body>Submission successful.</Toast.Body>
                </Toast>
            </ToastContainer>
        </Container>
    );
}

const BenchmarkSubmissionPage: Page = {
    path: '/benchmark-submission',
    component: BenchmarkSubmission,
    name: 'BenchmarkSubmission',
    displayName: 'Benchmark',
};

export default BenchmarkSubmissionPage;

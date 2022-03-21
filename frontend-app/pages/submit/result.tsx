import React, { ReactElement, useState } from 'react';
import { Card, Container, Toast, ToastContainer } from 'react-bootstrap';
import { ResultSubmitForm } from 'components/forms/resultSubmitForm';

/**
 * Page allowing users to submit new results.
 *
 * This is essentially just a page wrapper around ResultSubmitForm.
 *
 * @returns {React.ReactElement}
 * @constructor
 */
function ResultSubmission(): ReactElement {
    const [showSuccessToast, setShowSuccessToast] = useState(false);

    return (
        <Container>
            <h1>Upload Result</h1>
            <Card className='mb-2'>
                <Card.Body>
                    <ResultSubmitForm
                        onSuccess={() => {
                            setShowSuccessToast(true);
                        }}
                        onError={() => undefined}
                    />
                </Card.Body>
            </Card>
            <ToastContainer position='middle-center'>
                <Toast
                    show={showSuccessToast}
                    onClose={() => setShowSuccessToast(false)}
                    delay={4000}
                    autohide
                >
                    <Toast.Header>
                        <strong className='me-auto'>eosc-perf</strong>
                    </Toast.Header>
                    <Toast.Body>Submission successful.</Toast.Body>
                </Toast>
            </ToastContainer>
        </Container>
    );
}

export default ResultSubmission;

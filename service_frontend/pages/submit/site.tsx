import React, { ReactElement, useState } from 'react';
import { Card, Container, Toast, ToastContainer } from 'react-bootstrap';
import { SiteSubmitForm } from 'components/forms/siteSubmitForm';

/**
 * Page allowing users to submit new sites.
 *
 * This is essentially just a page wrapper around SiteSubmitForm.
 *
 * @returns {React.ReactElement}
 * @constructor
 */
function SiteSubmission(): ReactElement {
    const [showSuccessToast, setShowSuccessToast] = useState(false);

    return (
        <Container>
            <h1>Add Site</h1>
            <Card className='mb-2'>
                <Card.Body>
                    <SiteSubmitForm
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

export default SiteSubmission;

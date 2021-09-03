import React, { useContext, useState } from 'react';
import { Alert, Button, Form, Modal, Toast } from 'react-bootstrap';
import { useMutation } from 'react-query';
import { postHelper } from 'api-helpers';
import { SiteCreate } from 'api';
import { UserContext } from 'userContext';
import axios, { AxiosError } from 'axios';

// TODO: do not show invalid on first load
//       use default state valid?

export function SiteSubmissionModal(props: { show: boolean; onHide: () => void }) {
    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    const [description, setDescription] = useState('');

    const [showSuccessToast, setShowSuccessToast] = useState(false);
    const [errorMessage, setErrorMessage] = useState<string | undefined>(undefined);

    const auth = useContext(UserContext);

    const { mutate } = useMutation(
        (data: SiteCreate) => postHelper<SiteCreate>('/sites', data, auth.token),
        {
            onSuccess: () => {
                setShowSuccessToast(true);
                props.onHide();
            },
            onError: (error: Error | AxiosError) => {
                if (axios.isAxiosError(error)) {
                    if (error.response) {
                        switch (error.response.status) {
                            case 409:
                                setErrorMessage('Site already exists');
                                break;
                            case 422:
                            default:
                                setErrorMessage(
                                    'Could not process submission:' + error.response.data.message
                                );
                                break;
                        }
                    } else if (error.request) {
                        setErrorMessage('No response');
                    } else {
                        setErrorMessage(error.message);
                    }
                    // Access to config, request, and response
                } else {
                    // Just a stock error
                    setErrorMessage('Unknown error, check the console');
                }
            },
        }
    );

    function isNameValid() {
        return name.length > 0;
    }

    function isAddressValid() {
        return address.length > 0;
    }

    function isFormValid() {
        return isNameValid() && isAddressValid() && auth.token !== undefined;
    }

    function onSubmit() {
        if (!isFormValid()) {
            return;
        }
        mutate({
            name,
            address,
            description: description.length ? description : undefined,
        });
    }

    return (
        <>
            <Modal
                size="lg"
                show={props.show}
                onHide={props.onHide}
                onExited={() => setErrorMessage(undefined)}
            >
                <Modal.Header closeButton>Add Site</Modal.Header>
                <Modal.Body>
                    {auth.token === undefined && (
                        <Alert variant="danger">You must be logged in to submit new sites!</Alert>
                    )}
                    {errorMessage !== undefined && (
                        <Alert variant="danger">{'Error: ' + errorMessage}</Alert>
                    )}
                    <Form>
                        <Form.Group>
                            <Form.Label>Name:</Form.Label>
                            <Form.Control
                                placeholder="KIT SCC"
                                onChange={(e) => setName(e.target.value)}
                                isInvalid={!isNameValid()}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Address</Form.Label>
                            <Form.Control
                                placeholder="https://www.scc.kit.edu/"
                                onChange={(e) => setAddress(e.target.value)}
                                isInvalid={!isAddressValid()}
                            />
                        </Form.Group>
                        <Form.Label>Description (optional):</Form.Label>
                        <Form.Control
                            placeholder="Add a description here."
                            onChange={(e) => setDescription(e.target.value)}
                            as="textarea"
                        />
                        <Button
                            variant="success"
                            onClick={onSubmit}
                            disabled={!isFormValid()}
                            className="my-1"
                        >
                            Submit
                        </Button>
                    </Form>
                </Modal.Body>
            </Modal>
            <div style={{ position: 'fixed', bottom: 0, right: 0 }}>
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
            </div>
        </>
    );
}

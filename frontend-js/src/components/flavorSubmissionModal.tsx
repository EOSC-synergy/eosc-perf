import React, { useContext, useState } from 'react';
import { Alert, Button, Form, Modal, Toast } from 'react-bootstrap';
import { useMutation } from 'react-query';
import { postHelper } from '../api-helpers';
import { FlavorCreate, Site } from '../api';
import { UserContext } from '../userContext';
import axios, { AxiosError } from 'axios';

// TODO: do not show invalid on first load
//       use default state valid?

export function FlavorSubmissionModal(props: { show: boolean; onHide: () => void; site: Site }) {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');

    const [showSuccessToast, setShowSuccessToast] = useState(false);
    const [errorMessage, setErrorMessage] = useState<string | undefined>(undefined);

    const auth = useContext(UserContext);

    const { mutate } = useMutation(
        (data: FlavorCreate) =>
            postHelper<FlavorCreate>('/sites/' + props.site.id + '/flavors', data, auth.token),
        {
            onSuccess: (data) => {
                setShowSuccessToast(true);
                props.onHide();
            },
            onError: (error: Error | AxiosError) => {
                if (axios.isAxiosError(error)) {
                    if (error.response) {
                        switch (error.response.status) {
                            case 409:
                                setErrorMessage('Flavor already exists');
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

    function isFormValid() {
        return isNameValid() && auth.token !== undefined;
    }

    function onSubmit() {
        if (!isFormValid()) {
            return;
        }
        mutate({
            name,
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
                        <Alert variant="danger">
                            You must be logged in to submit new site flavors!
                        </Alert>
                    )}
                    {errorMessage !== undefined && (
                        <Alert variant="danger">{'Error: ' + errorMessage}</Alert>
                    )}
                    <Form>
                        <Form.Group>
                            <Form.Label>Name:</Form.Label>
                            <Form.Control
                                placeholder="standard-medium"
                                onChange={(e) => setName(e.target.value)}
                                isInvalid={!isNameValid()}
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
                        <strong className="mr-auto">eosc-perf</strong>
                    </Toast.Header>
                    <Toast.Body>Submission successful.</Toast.Body>
                </Toast>
            </div>
        </>
    );
}

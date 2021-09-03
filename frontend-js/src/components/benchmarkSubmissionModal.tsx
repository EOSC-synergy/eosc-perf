import React, { useContext, useState } from 'react';
import { Alert, Button, Form, Modal, Toast } from 'react-bootstrap';
import { useMutation } from 'react-query';
import { postHelper } from '../api-helpers';
import { BenchmarkCreate } from '../api';
import { UserContext } from '../userContext';
import axios, { AxiosError } from 'axios';

// TODO: do not show invalid on first load
//       use default state valid?

export function BenchmarkSubmissionModal(props: { show: boolean; onHide: () => void }) {
    const [dockerName, setDockerName] = useState('');
    const [dockerTag, setDockerTag] = useState('');
    const [template, setTemplate] = useState('');
    const [description, setDescription] = useState('');
    const [showSuccessToast, setShowSuccessToast] = useState(false);

    const [errorMessage, setErrorMessage] = useState<string | undefined>(undefined);

    const auth = useContext(UserContext);

    const { mutate } = useMutation(
        (data: BenchmarkCreate) => postHelper<BenchmarkCreate>('/benchmarks', data, auth.token),
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
                                setErrorMessage('Benchmark already exists');
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

    function isDockerNameValid() {
        // match pattern (...)/(...)
        return dockerName.match(/[^\/]+\/[^\/]+/);
    }

    function isDockerTagValid() {
        return dockerTag.length >= 1;
    }

    function isTemplateValid() {
        if (template.length == 0) {
            return true;
        }
        try {
            JSON.parse(template);
            return true;
        } catch (SyntaxError) {
            return false;
        }
    }

    function isFormValid() {
        return (
            isDockerNameValid() &&
            isDockerTagValid() &&
            isTemplateValid() &&
            auth.token !== undefined
        );
    }

    function onSubmit() {
        if (!isFormValid()) {
            return;
        }
        const description_ = description && description.length ? description : undefined;
        const template_ = template && template.length ? template : undefined;
        mutate({
            docker_image: dockerName,
            docker_tag: dockerTag,
            description: description_,
            json_schema: template_,
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
                <Modal.Header closeButton>Add Benchmark</Modal.Header>
                <Modal.Body>
                    {auth.token === undefined && (
                        <Alert variant="danger">
                            You must be logged in to submit new benchmarks!
                        </Alert>
                    )}
                    {errorMessage !== undefined && (
                        <Alert variant="danger">{'Error: ' + errorMessage}</Alert>
                    )}
                    <Form>
                        {/* TODO: side-by-side, with infix : */}
                        <Form.Group>
                            <Form.Label htmlFor="docker_name">Docker image name:</Form.Label>
                            <Form.Control
                                name="docker_name"
                                id="docker_name"
                                placeholder="user/image"
                                onChange={(e) => setDockerName(e.target.value)}
                                isInvalid={!isDockerNameValid()}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Control
                                name="docker_tag"
                                id="docker_tag"
                                placeholder="tag"
                                onChange={(e) => setDockerTag(e.target.value)}
                                isInvalid={!isDockerTagValid()}
                            />
                        </Form.Group>
                        <Form.Label htmlFor="docker_name">
                            Benchmark description (optional):
                        </Form.Label>
                        <Form.Control
                            name="description"
                            id="description"
                            placeholder="Enter a description of the new benchmark here."
                            onChange={(e) => setDescription(e.target.value)}
                            as="textarea"
                        />
                        <Form.Label htmlFor="template">
                            Benchmark result JSON template (optional,{' '}
                            {/* TODO: react-router-hash-link */}
                            <a href="/code-guidelines#json">example here</a>):
                        </Form.Label>
                        <Form.Control
                            name="template"
                            id="template"
                            placeholder='{ "required_arg": 5, "!notable_argument": 10 }'
                            onChange={(e) => setTemplate(e.target.value)}
                            as="textarea"
                            isInvalid={!isTemplateValid()}
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

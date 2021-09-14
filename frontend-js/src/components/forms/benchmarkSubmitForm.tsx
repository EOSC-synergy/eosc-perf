import { Alert, Button, Form } from 'react-bootstrap';
import pages from 'pages';
import React, { ReactElement, useContext, useEffect, useState } from 'react';
import { UserContext } from 'userContext';
import { useMutation } from 'react-query';
import { BenchmarkCreate } from 'api';
import { postHelper } from 'api-helpers';
import axios, { AxiosError } from 'axios';

// TODO: do not show invalid on first load
//       use default state valid?

export function BenchmarkSubmitForm(props: {
    onSuccess: () => void;
    onError: () => void;
}): ReactElement {
    const auth = useContext(UserContext);

    const [dockerName, setDockerName] = useState('');
    const [dockerTag, setDockerTag] = useState('');
    const [template, setTemplate] = useState('');
    const [description, setDescription] = useState('');

    const [errorMessage, setErrorMessage] = useState<string | undefined>(undefined);

    // clear error message on load
    useEffect(() => {
        setErrorMessage(undefined);
    }, []);

    const { mutate } = useMutation(
        (data: BenchmarkCreate) => postHelper<BenchmarkCreate>('/benchmarks', data, auth.token),
        {
            onSuccess: () => {
                props.onSuccess();
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
                props.onError();
            },
        }
    );

    function isDockerNameValid() {
        // match pattern (...)/(...)
        return dockerName.match(/[^/]+\/[^/]+/);
    }

    function isDockerTagValid() {
        return dockerTag.length >= 1;
    }

    function isTemplateValid() {
        if (template.length === 0) {
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
            {auth.token === undefined && (
                <Alert variant="danger">You must be logged in to submit new benchmarks!</Alert>
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
                <Form.Label htmlFor="docker_name">Benchmark description (optional):</Form.Label>
                <Form.Control
                    name="description"
                    id="description"
                    placeholder="Enter a description of the new benchmark here."
                    onChange={(e) => setDescription(e.target.value)}
                    as="textarea"
                />
                <Form.Label htmlFor="template">
                    Benchmark result JSON template (optional, {/* TODO: react-router-hash-link */}
                    <a href={pages.CodeGuidelinesModule.path + '#json'}>example here</a>):
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
        </>
    );
}

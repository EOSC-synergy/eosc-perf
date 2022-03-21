import { Alert, Button, Form, InputGroup } from 'react-bootstrap';
import React, { ReactElement, ReactNode, useContext, useEffect, useState } from 'react';
import { UserContext } from 'components/userContext';
import { useMutation } from 'react-query';
import { CreateBenchmark } from 'api';
import { postHelper } from 'api-helpers';
import { AxiosError } from 'axios';
import { NavLink } from 'react-router-dom';
import { getErrorMessage } from 'components/forms/getErrorMessage';
import benchmarkJsonSchema from '../benchmarkJsonSchema.json';
import { RegistrationCheck } from 'components/registrationCheck';
import CodeGuidelinesPage from 'pages/codeGuidelines';

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

    const [errorMessage, setErrorMessage] = useState<ReactNode | undefined>(undefined);

    // clear error message on load
    useEffect(() => {
        setErrorMessage(undefined);
    }, []);

    const { mutate } = useMutation(
        (data: CreateBenchmark) => postHelper<CreateBenchmark>('/benchmarks', data, auth.token),
        {
            onSuccess: () => {
                props.onSuccess();
            },
            onError: (error: Error | AxiosError) => {
                setErrorMessage(getErrorMessage(error));
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
        const description_ = description && description.length ? description : null;
        const template_ = template && template.length ? template : undefined;
        mutate({
            docker_image: dockerName,
            docker_tag: dockerTag,
            description: description_,
            json_schema: template_ ? JSON.parse(template_) : undefined,
        });
    }

    return (
        <>
            {auth.token === undefined && (
                <Alert variant="danger">You must be logged in to submit new benchmarks!</Alert>
            )}
            {errorMessage !== undefined && <Alert variant="danger">Error: {errorMessage}</Alert>}
            <RegistrationCheck />
            <Form>
                <Form.Group className="mb-3">
                    <Form.Label htmlFor="benchmark">Benchmark:</Form.Label>
                    <InputGroup>
                        <Form.Control
                            placeholder="user/image"
                            onChange={(e) => setDockerName(e.target.value)}
                            isInvalid={!isDockerNameValid()}
                            aria-label="Docker image name including username"
                            id="benchmark"
                        />
                        <InputGroup.Text>:</InputGroup.Text>
                        <Form.Control
                            placeholder="tag"
                            onChange={(e) => setDockerTag(e.target.value)}
                            isInvalid={!isDockerTagValid()}
                            aria-label="Tag or version of the docker image to use"
                        />
                    </InputGroup>
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label htmlFor="description">Benchmark description (optional):</Form.Label>
                    <Form.Control
                        id="description"
                        placeholder="Enter a description of the new benchmark here."
                        onChange={(e) => setDescription(e.target.value)}
                        as="textarea"
                    />
                </Form.Group>

                <Form.Group>
                    <Form.Label htmlFor="template">
                        Benchmark result JSON schema (optional,{' '}
                        <NavLink to={CodeGuidelinesPage.path + '#json'}>example here</NavLink>
                        ):
                    </Form.Label>
                    <Form.Control
                        id="template"
                        placeholder={JSON.stringify(benchmarkJsonSchema, null, 4)}
                        onChange={(e) => setTemplate(e.target.value)}
                        as="textarea"
                        isInvalid={!isTemplateValid()}
                    />
                </Form.Group>

                <Button
                    variant="success"
                    onClick={onSubmit}
                    disabled={!isFormValid()}
                    className="mt-1"
                >
                    Submit
                </Button>
            </Form>
        </>
    );
}

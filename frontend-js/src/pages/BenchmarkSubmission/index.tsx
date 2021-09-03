import React, { useContext, useState } from 'react';
import { Button, Container, Form } from 'react-bootstrap';
import { useMutation } from 'react-query';
import { postHelper } from 'api-helpers';
import { BenchmarkCreate } from 'api';
import { UserContext } from 'userContext';
import { PageBase } from '../pageBase';

// TODO: do not show invalid on first load
//       use default state valid?

function BenchmarkSubmission() {
    const [dockerName, setDockerName] = useState('');
    const [dockerTag, setDockerTag] = useState('');
    const [template, setTemplate] = useState('');
    const [description, setDescription] = useState('');

    const auth = useContext(UserContext);

    const { mutate } = useMutation(
        (data: BenchmarkCreate) => postHelper<BenchmarkCreate>('/benchmarks', data, auth.token),
        {
            onSuccess: () => {},
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
        return isDockerNameValid() && isDockerTagValid() && isTemplateValid();
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
        <Container>
            <h1>Add Benchmark</h1>
            <Form>
                <div className="m-2">
                    {/* TODO: side-by-side, with infix . */}
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
                </div>
                <div className="m-2">
                    <Form.Label htmlFor="docker_name">Benchmark description (optional):</Form.Label>
                    <Form.Control
                        name="description"
                        id="description"
                        placeholder="Enter a description of the new benchmark here."
                        onChange={(e) => setDescription(e.target.value)}
                        as="textarea"
                    />
                </div>
                <div className="m-2">
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
                </div>
                <Button variant="success" onClick={onSubmit} disabled={!isFormValid()}>
                    Submit
                </Button>
            </Form>
        </Container>
    );
}

const BenchmarkSubmissionModule: PageBase = {
    path: '/benchmark-submission',
    element: BenchmarkSubmission,
    name: 'BenchmarkSubmission',
    displayName: 'Benchmark',
};

export default BenchmarkSubmissionModule;

import React, { ReactElement } from 'react';
import { Container } from 'react-bootstrap';
import template from 'components/benchmarkJsonSchema.json';
import { PageBase } from '../pageBase';
import Highlight from 'react-highlight';

function CodeGuidelines(): ReactElement {
    return (
        <Container>
            <h1>Code Guidelines</h1>
            <h2>Availability</h2>
            <p>
                The Benchmark has to be publicly available on{' '}
                <a href="https://hub.docker.com/">Docker Hub</a>.
            </p>
            <h2>Result Json</h2>
            <p>
                You may submit templates for the results as JSON Schemas to prevent unrelated or
                invalid JSON files from being uploaded. Below is a example JSON schema, which is
                containing the minimum set of required output parameters.
            </p>
            <p>
                You may learn more about writing <a href="https://json-schema.org/">JSON Schema</a>{' '}
                templates at:
                <ul>
                    <li>
                        <a href="https://json-schema.org/learn/getting-started-step-by-step">
                            https://json-schema.org/learn/getting-started-step-by-step
                        </a>
                    </li>
                    <li>
                        <a href="https://json-schema.org/understanding-json-schema/basics.html">
                            https://json-schema.org/understanding-json-schema/basics.html
                        </a>
                    </li>
                </ul>
            </p>
            <p>
                To have a field show up as a suggested field to the user for filtering, add{' '}
                <code>&quot;suggestToUser&quot;: true</code> to the property in JSON Schema, like in
                the example below.
            </p>
            <p>Example template:</p>
            <div className="m-2">
                <Highlight className="json">{JSON.stringify(template, null, 4)}</Highlight>
            </div>
        </Container>
    );
}

const CodeGuidelinesModule: PageBase = {
    path: '/code-guidelines',
    element: CodeGuidelines,
    name: 'CodeGuidelines',
    displayName: 'Code guidelines',
};

export default CodeGuidelinesModule;

import React from 'react';
import { Container } from 'react-bootstrap';
import template from './benchmark_template.json';
import { PageBase } from '../pageBase';

function CodeGuidelines() {
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
                Below is a example JSON, which is containing the minimum set of required output
                parameters.
            </p>
            <p>
                Keys prefixed with <code>!</code> are recognized as notable keys. Notable keys are a
                select subset of all keys that may be noteworthy for result comparisons. These keys
                will be shown as suggestions as a dropdown in the JSON filter, and can be used as
                fields in the line graph. The exclamation point will <i>not</i> be considered part
                of the key name.
            </p>
            <p>
                Example: <code>{'{"group": {"!key": value}}'}</code> refers to{' '}
                <code>{'{"group": {"key": value}}'}</code>/ <code>group.key</code>.
            </p>
            <p>Example template:</p>
            <div className="m-2">
                <code>
                    <span style={{ whiteSpace: 'pre-wrap' }}>
                        {JSON.stringify(template, null, 4)}
                    </span>
                </code>
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

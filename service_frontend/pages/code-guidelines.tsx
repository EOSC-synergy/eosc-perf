import React, { ReactElement } from 'react';
import { Container } from 'react-bootstrap';
import template from 'components/benchmarkJsonSchemaExample.json';
import { JsonHighlight } from 'components/jsonHighlight';
import Head from 'next/head';

/**
 * Guidelines page for developers creating and submitting new benchmarks to the site.
 *
 * @returns {React.ReactElement}
 * @constructor
 */
function CodeGuidelines(): ReactElement {
    return (
        <>
            <Head>
                <title>Code Guidelines</title>
            </Head>
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
                <p style={{ marginBottom: '0em' }}>
                    You may learn more about writing{' '}
                    <a href="https://json-schema.org/">JSON Schema</a> templates at:
                </p>
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
                <p>
                    To have a field show up as a suggested field to the user for filtering, add{' '}
                    <code>&quot;suggestToUser&quot;: true</code> to the property in JSON Schema,
                    like in the example below.
                </p>
                <p>Example template:</p>
                <div className="m-2">
                    <JsonHighlight>{JSON.stringify(template, null, 4)}</JsonHighlight>
                </div>
            </Container>
        </>
    );
}

export default CodeGuidelines;

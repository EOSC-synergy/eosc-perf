import { JsonHighlight } from './jsonHighlight';
import { render, screen } from '@testing-library/react';

import jsonSchemaExample from './benchmarkJsonSchemaExample.json';

describe('json highlight', () => {
    test('contains expected data', () => {
        render(
            <>
                <JsonHighlight>{JSON.stringify(jsonSchemaExample)}</JsonHighlight>
            </>
        );
        expect(screen.getByText('hz_actual_friendly', { exact: false })).toBeInTheDocument();
    });
});

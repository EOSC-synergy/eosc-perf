import { ResultsPerPageSelection } from './resultsPerPageSelection';
import { render } from '@testing-library/react';

describe('results per page selection', () => {
    test('valid option', () => {
        const onChange = jest.fn();
        const { container } = render(
            <>
                <ResultsPerPageSelection onChange={onChange} currentSelection={50} />
            </>
        );
        expect((container.querySelector('option:checked') as HTMLOptionElement).value).toBe('50');
    });
    test('invalid option', () => {
        const onChange = jest.fn();
        const { container } = render(
            <>
                <ResultsPerPageSelection onChange={onChange} currentSelection={621} />
            </>
        );
        expect((container.querySelector('option:checked') as HTMLOptionElement).value).toBe('10');
    });
});

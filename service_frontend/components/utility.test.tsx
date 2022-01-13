import { benchmarkLinkDisplay, truthyOrNoneTag } from './utility';
import { render, screen } from '@testing-library/react';
import { benchmark } from './testData';

describe('truthy or none tag', () => {
    test('truthy', () => {
        render(<div data-testid="contents">{truthyOrNoneTag('toothpaste')}</div>);

        const content = screen.getByText('toothpaste');
        expect(content).toBeInTheDocument();
    });
    test('falsy', () => {
        render(<div data-testid="contents">{truthyOrNoneTag('')}</div>);

        const content = screen.getByText('None');
        expect(content).toBeInTheDocument();
    });
});

describe('benchmark link display', () => {
    test('test', () => {
        render(<div>{benchmarkLinkDisplay(benchmark)}</div>);

        expect(screen.getByText('__bench_image__')).toBeInTheDocument();
        expect(screen.getByText('__bench_tag__', { exact: false })).toBeInTheDocument();
    });
});

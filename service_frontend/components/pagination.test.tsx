import { act, render, screen } from '@testing-library/react';
import { Paginatable, Paginator } from './pagination';

describe('pagination', () => {
    const pagination: Paginatable = {
        has_next: false,
        has_prev: false,
        next_num: 5,
        pages: 7,
        prev_num: 3,
        total: 7,
    };

    test('first', () => {
        const onChange = jest.fn();
        render(
            <>
                <Paginator navigateTo={onChange} pagination={pagination} />{' '}
            </>
        );
        act(() => {
            screen.getByTestId('paginator-first').click();
        });

        expect(onChange).toHaveBeenCalledWith(1);
    });
    test('prev', () => {
        const onChange = jest.fn();
        render(
            <>
                <Paginator navigateTo={onChange} pagination={pagination} />{' '}
            </>
        );
        act(() => {
            screen.getByTestId('paginator-prev').click();
        });

        expect(onChange).toHaveBeenCalledWith(3);
    });
    test('next', () => {
        const onChange = jest.fn();
        render(
            <>
                <Paginator navigateTo={onChange} pagination={pagination} />{' '}
            </>
        );
        act(() => {
            screen.getByTestId('paginator-next').click();
        });

        expect(onChange).toHaveBeenCalledWith(5);
    });
    test('last', () => {
        const onChange = jest.fn();
        render(
            <>
                <Paginator navigateTo={onChange} pagination={pagination} />{' '}
            </>
        );
        act(() => {
            screen.getByTestId('paginator-last').click();
        });

        expect(onChange).toHaveBeenCalledWith(7);
    });

    test('specific', () => {
        const onChange = jest.fn();
        render(
            <>
                <Paginator navigateTo={onChange} pagination={pagination} />{' '}
            </>
        );
        act(() => {
            screen.getByText('6').click();
        });

        expect(onChange).toHaveBeenCalledWith(6);
    });
});

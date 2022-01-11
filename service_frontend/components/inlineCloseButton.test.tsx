import React from 'react';
import { InlineCloseButton } from 'components/inlineCloseButton';
import { act, render, screen } from '@testing-library/react';

test('interaction', () => {
    const onClick = jest.fn();
    render(<InlineCloseButton onClose={onClick} />);
    const linkElement = screen.getByRole('button');

    act(() => linkElement.click());
    expect(onClick).toHaveBeenCalled();
});

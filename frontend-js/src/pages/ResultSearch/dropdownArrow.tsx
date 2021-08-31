import React from 'react';

export function DropdownArrow(props: { toggled: boolean }) {
    return <span className={'dropdown-arrow' + (props.toggled ? ' opened' : '')} />;
}

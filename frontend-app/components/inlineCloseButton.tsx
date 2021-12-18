import React, { ReactElement } from 'react';
import { X } from 'react-bootstrap-icons';
import actionable from 'styles/actionable.module.css';

export function InlineCloseButton(props: { onClose: () => void }): ReactElement {
    return (
        <div onClick={() => props.onClose()} className={'d-inline-block' + actionable.actionable} role='button'>
            <X />
        </div>
    );
}

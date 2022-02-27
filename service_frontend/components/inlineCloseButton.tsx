import React, { ReactElement } from 'react';
import { X } from 'react-bootstrap-icons';
import actionable from 'styles/actionable.module.css';

/**
 * Small X button representing a close action that is rendered inline
 * @param props.onClose callback to call when button is pressed
 * @constructor
 */
export function InlineCloseButton(props: { onClose: () => void }): ReactElement {
    return (
        <div
            onClick={() => props.onClose()}
            className={'d-inline-block ' + actionable.actionable}
            role="button"
        >
            <X />
        </div>
    );
}

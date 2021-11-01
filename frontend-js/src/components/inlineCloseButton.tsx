import React, { ReactElement } from 'react';
import { X } from 'react-bootstrap-icons';

export function InlineCloseButton(props: { onClose: () => void }): ReactElement {
    return (
        <div onClick={() => props.onClose()} className="d-inline-block actionable" role="button">
            <X />
        </div>
    );
}

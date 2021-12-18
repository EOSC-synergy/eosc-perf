import React, { ReactElement } from 'react';

export function LoadingOverlay(): ReactElement {
    return (
        <div
            className='overlay loading-background loading center-contents'
            id='loadingIcon'
        >
            <div className='lds-ellipsis'>
                <div />
                <div />
                <div />
                <div />
            </div>
        </div>
    );
}

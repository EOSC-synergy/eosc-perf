import React from 'react';
import '../main.css';
import '../pages/loading.css';

export function LoadingOverlay(props: {}) {
    return (
        <div className="overlay loading-background loading center-contents" id="loadingIcon">
            <div className="lds-ellipsis">
                <div />
                <div />
                <div />
                <div />
            </div>
        </div>
    );
}

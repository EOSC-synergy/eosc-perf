import React, { ReactElement } from 'react';

import style from 'styles/loadingOverlay.module.css';

/**
 * Space filling loading overlay including a spinner or equivalent
 * @constructor
 */
export function LoadingOverlay(): ReactElement {
    return (
        <div className={style.loading}>
            <div className={style.ldsEllipsis}>
                <div />
                <div />
                <div />
                <div />
            </div>
        </div>
    );
}

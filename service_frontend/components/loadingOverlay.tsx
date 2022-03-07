import React, { ReactElement, ReactNode } from 'react';

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

export function LoadingWrapper({
    isLoading,
    children,
}: {
    isLoading: boolean;
    children: ReactNode;
}) {
    if (isLoading) {
        return <LoadingOverlay />;
    }
    return <>{children}</>;
}

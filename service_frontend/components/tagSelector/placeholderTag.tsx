import React, { ReactElement } from 'react';
import style from 'styles/tagSelector.module.css';
import { Placeholder } from 'react-bootstrap';

/**
 * Placeholder tag component for use when tags are still loading
 * @constructor
 */
export function PlaceholderTag(): ReactElement {
    return (
        <div className={style.tagBadge + 'p-1'}>
            <Placeholder xs={12} style={{ width: '2em' }} />
        </div>
    );
}

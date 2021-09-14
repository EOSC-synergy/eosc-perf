import React, { ReactElement } from 'react';
import { Result } from 'api';

export function TagsColumn(props: { result: Result }): ReactElement {
    return (
        <>
            {props.result.tags.length ? (
                props.result.tags.join(', ')
            ) : (
                <div className="text-muted">None</div>
            )}
        </>
    );
}

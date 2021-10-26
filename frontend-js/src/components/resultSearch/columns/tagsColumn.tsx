import React, { ReactElement } from 'react';
import { Result } from 'api';
import { Ordered } from 'components/ordered';

export function TagsColumn(props: { result: Ordered<Result> }): ReactElement {
    return (
        <>
            {props.result.tags.length ? (
                props.result.tags.map((tag) => tag.name).join(', ')
            ) : (
                <div className="text-muted">None</div>
            )}
        </>
    );
}

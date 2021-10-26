import React, { ReactElement } from 'react';
import { Result } from 'api';
import { fetchSubkey } from 'components/resultSearch/jsonKeyHelpers';
import { Ordered } from 'components/ordered';

export function CustomColumn(props: { result: Ordered<Result>; jsonKey: string }): ReactElement {
    const value = fetchSubkey(props.result.json, props.jsonKey) as string | number;
    return <>{value ? value.toString() : <div className="text-muted">Not found!</div>}</>;
}

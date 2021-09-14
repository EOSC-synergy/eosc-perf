import React, { ReactElement } from 'react';
import { Result } from 'api';
import { fetchSubkey } from '../jsonKeyHelpers';

export function CustomColumn(props: { result: Result; jsonKey: string }): ReactElement {
    const value = fetchSubkey(props.result.json, props.jsonKey) as string | number;
    return <>{value ? value.toString() : <div className="text-muted">Not found!</div>}</>;
}

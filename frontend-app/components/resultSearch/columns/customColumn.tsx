import React, { ReactElement } from 'react';
import { Result } from 'model';
import { fetchSubkey } from 'components/resultSearch/jsonKeyHelpers';
import { Ordered } from 'components/ordered';
import { truthyOrNoneTag } from 'components/utility';

export function CustomColumn(props: {
    result: Ordered<Result>;
    jsonKey: string;
}): ReactElement {
    const value = fetchSubkey(props.result.json, props.jsonKey) as
        | string
        | number;
    return <>{truthyOrNoneTag(value?.toString(), 'Not found!')}</>;
}

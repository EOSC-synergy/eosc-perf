import React, { ReactElement } from 'react';
import { Result } from 'api';
import { fetchSubkey } from 'components/resultSearch/jsonKeyHelpers';
import { Ordered } from 'components/ordered';
import { truthyOrNoneTag } from 'utility';

export function CustomColumn(props: { result: Ordered<Result>; jsonKey: string }): ReactElement {
    const value = fetchSubkey(props.result.json, props.jsonKey) as string | number;
    return <>{truthyOrNoneTag(value.toString(), 'Not found!')}</>;
}

import React, { ReactElement } from 'react';
import { Result } from 'model';
import { fetchSubkey } from 'components/resultSearch/jsonKeyHelpers';
import { Ordered } from 'components/ordered';
import { truthyOrNoneTag } from 'components/utility';

/**
 * Column to display specified JSON-value
 * @param {Result & {orderIndex: number}} result
 * @param {string} jsonKey Key to JSON value to display
 * @returns {React.ReactElement}
 * @constructor
 */
export function CustomColumn({
    result,
    jsonKey,
}: {
    result: Ordered<Result>;
    jsonKey: string;
}): ReactElement {
    const value = fetchSubkey(result.json, jsonKey) as string | number;
    return <>{truthyOrNoneTag(value?.toString(), 'Not found!')}</>;
}

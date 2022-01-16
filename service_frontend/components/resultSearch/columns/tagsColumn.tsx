import React, { ReactElement } from 'react';
import { Result } from 'model';
import { Ordered } from 'components/ordered';
import { truthyOrNoneTag } from 'components/utility';

/**
 * Column to display a list of tags associated to result
 * @param {Result & {orderIndex: number}} result
 * @returns {React.ReactElement}
 * @constructor
 */
export function TagsColumn({ result }: { result: Ordered<Result> }): ReactElement {
    return <>{truthyOrNoneTag(result.tags.map((tag) => tag.name).join(', '))}</>;
}

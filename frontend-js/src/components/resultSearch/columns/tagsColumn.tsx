import React, { ReactElement } from 'react';
import { Result } from 'api';
import { Ordered } from 'components/ordered';
import { truthyOrNoneTag } from 'utility';

export function TagsColumn(props: { result: Ordered<Result> }): ReactElement {
    return <>{truthyOrNoneTag(props.result.tags.map((tag) => tag.name).join(', '))}</>;
}

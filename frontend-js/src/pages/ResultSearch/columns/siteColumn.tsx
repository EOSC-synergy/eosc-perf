import React, { ReactElement } from 'react';
import { Result } from 'api';
import { Ordered } from 'components/ordered';

export function SiteColumn(props: { result: Ordered<Result> }): ReactElement {
    return <>{props.result.site.name}</>;
}

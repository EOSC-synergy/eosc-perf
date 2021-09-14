import React, { ReactElement } from 'react';
import { Result } from 'api';

export function SiteColumn(props: { result: Result }): ReactElement {
    return <>{props.result.site.name}</>;
}

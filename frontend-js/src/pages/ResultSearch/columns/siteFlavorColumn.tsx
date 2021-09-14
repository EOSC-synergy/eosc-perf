import React, { ReactElement } from 'react';
import { Result } from 'api';

export function SiteFlavorColumn(props: { result: Result }): ReactElement {
    return <>{props.result.flavor.name}</>;
}

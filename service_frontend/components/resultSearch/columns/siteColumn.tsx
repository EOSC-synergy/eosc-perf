import React, { ReactElement } from 'react';
import { Result } from 'model';
import { Ordered } from 'components/ordered';

/**
 * Column to display execution site
 * @param {Result & {orderIndex: number}} result
 * @returns {React.ReactElement}
 * @constructor
 */
export function SiteColumn({ result }: { result: Ordered<Result> }): ReactElement {
    return <>{result.site.name}</>;
}

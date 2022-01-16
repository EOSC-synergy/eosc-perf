import React, { ReactElement } from 'react';
import { Result } from 'model';
import { Ordered } from 'components/ordered';

/**
 * Column to display execution site machine flavor
 * @param {Result & {orderIndex: number}} result
 * @returns {React.ReactElement}
 * @constructor
 */
export function SiteFlavorColumn({ result }: { result: Ordered<Result> }): ReactElement {
    return <>{result.flavor.name}</>;
}

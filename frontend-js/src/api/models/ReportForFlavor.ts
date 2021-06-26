/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Flavor } from './Flavor';
import type { Site } from './Site';

export type ReportForFlavor = {
    verdict?: boolean;
    readonly site?: Site;
    readonly flavor?: Flavor;
    readonly date?: string;
    verified?: boolean;
    readonly id?: string;
    message: string;
}

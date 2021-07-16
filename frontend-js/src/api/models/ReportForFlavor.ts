/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Flavor } from './Flavor';
import type { Site } from './Site';

export type ReportForFlavor = {
    readonly flavor?: Flavor;
    verified?: boolean;
    verdict?: boolean;
    readonly date?: string;
    readonly id?: string;
    readonly site?: Site;
    message: string;
}

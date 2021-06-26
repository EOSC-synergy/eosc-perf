/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Site } from './Site';

export type ReportForSite = {
    verdict?: boolean;
    readonly site?: Site;
    readonly date?: string;
    verified?: boolean;
    readonly id?: string;
    message: string;
}

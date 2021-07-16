/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Site } from './Site';

export type ReportForSite = {
    verified?: boolean;
    verdict?: boolean;
    readonly date?: string;
    readonly id?: string;
    readonly site?: Site;
    message: string;
}

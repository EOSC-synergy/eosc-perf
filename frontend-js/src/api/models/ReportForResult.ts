/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Result } from './Result';

export type ReportForResult = {
    verified?: boolean;
    verdict?: boolean;
    readonly date?: string;
    readonly id?: string;
    readonly result?: Result;
    message: string;
}

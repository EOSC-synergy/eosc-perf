/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Result } from './Result';

export type ReportForResult = {
    readonly result?: Result;
    verdict?: boolean;
    readonly date?: string;
    verified?: boolean;
    readonly id?: string;
    message: string;
}

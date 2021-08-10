/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Report } from './Report';

export type Reports = {
    readonly prev_num: number;
    readonly total: number;
    per_page?: number;
    readonly next_num: number;
    readonly has_next: boolean;
    items?: Array<Report>;
    readonly pages: number;
    page?: number;
    readonly has_prev: boolean;
}

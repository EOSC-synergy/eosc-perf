/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Site } from './Site';

export type Sites = {
    readonly prev_num: number;
    readonly total: number;
    per_page?: number;
    readonly next_num: number;
    readonly has_next: boolean;
    items?: Array<Site>;
    readonly pages: number;
    page?: number;
    readonly has_prev: boolean;
}

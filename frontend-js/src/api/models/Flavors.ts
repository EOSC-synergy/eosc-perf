/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Flavor } from './Flavor';

export type Flavors = {
    readonly prev_num: number;
    readonly total: number;
    per_page?: number;
    readonly next_num: number;
    readonly has_next: boolean;
    items?: Array<Flavor>;
    readonly pages: number;
    page?: number;
    readonly has_prev: boolean;
}

/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Benchmark } from './Benchmark';

export type Benchmarks = {
    readonly prev_num: number;
    readonly total: number;
    per_page?: number;
    readonly next_num: number;
    readonly has_next: boolean;
    items?: Array<Benchmark>;
    readonly pages: number;
    page?: number;
    readonly has_prev: boolean;
}

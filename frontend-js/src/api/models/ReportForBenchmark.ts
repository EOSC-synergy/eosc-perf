/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Benchmark } from './Benchmark';

export type ReportForBenchmark = {
    verdict?: boolean;
    readonly date?: string;
    verified?: boolean;
    readonly benchmark?: Benchmark;
    readonly id?: string;
    message: string;
}

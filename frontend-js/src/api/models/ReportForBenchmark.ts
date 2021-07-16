/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Benchmark } from './Benchmark';

export type ReportForBenchmark = {
    verified?: boolean;
    verdict?: boolean;
    readonly date?: string;
    readonly benchmark?: Benchmark;
    readonly id?: string;
    message: string;
}

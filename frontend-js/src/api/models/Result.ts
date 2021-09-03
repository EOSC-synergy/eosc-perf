/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Benchmark } from './Benchmark';
import type { Flavor } from './Flavor';
import type { Site } from './Site';
import type { Tag } from './Tag';

export type Result = {
    /**
     * UUID resource unique identification
     */
    readonly id: string;
    json: any;
    /**
     * ISO8601 Datatime of the resource upload
     */
    upload_datetime: string;
    /**
     * ISO8601 Datatime of benchmark execution start
     */
    execution_datetime: string;
    benchmark: Benchmark;
    site: Site;
    flavor: Flavor;
    tags: Array<Tag>;
}

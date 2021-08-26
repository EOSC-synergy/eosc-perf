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
    upload_date: string;
    json: any;
    benchmark: Benchmark;
    site: Site;
    flavor: Flavor;
    tags: Array<Tag>;
}

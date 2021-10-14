/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Benchmark } from './Benchmark';
import type { Flavor } from './Flavor';
import type { Site } from './Site';
import type { Tag } from './Tag';

export type Result = {
    /**
     * Upload datetime of the referred resource
     */
    readonly upload_datetime: string;
    /**
     * UUID resource unique identification
     */
    readonly id: string;
    /**
     * START execution datetime of the result
     */
    execution_datetime: string;
    benchmark: Benchmark;
    site: Site;
    flavor: Flavor;
    tags: Array<Tag>;
    json: any;
};

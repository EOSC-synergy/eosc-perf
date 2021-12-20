/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Benchmark } from 'model/models/Benchmark';
import type { Flavor } from 'model/models/Flavor';
import type { Site } from 'model/models/Site';
import type { Tag } from 'model/models/Tag';

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

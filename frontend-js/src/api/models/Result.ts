/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Benchmark } from './Benchmark';
import type { Flavor } from './Flavor';
import type { Site } from './Site';
import type { Tag } from './Tag';

export type Result = {
    benchmark: Benchmark;
    site: Site;
    readonly id: string;
    tags: Array<Tag>;
    upload_date: string;
    flavor: Flavor;
    json: any;
}

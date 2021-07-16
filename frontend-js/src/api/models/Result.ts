/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Benchmark } from './Benchmark';
import type { Flavor } from './Flavor';
import type { Site } from './Site';
import type { Tag } from './Tag';

export type Result = {
    json: any;
    flavor?: Flavor;
    readonly upload_date?: string;
    benchmark?: Benchmark;
    readonly id?: string;
    tags?: Array<Tag>;
    site?: Site;
}

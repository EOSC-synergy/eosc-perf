/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Flavor } from './Flavor';

export type Site = {
    description?: string;
    address: string;
    name: string;
    flavors?: Array<Flavor>;
    readonly id?: string;
}

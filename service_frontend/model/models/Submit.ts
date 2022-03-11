/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User } from './User';

export type Submit = {
    /**
     * Upload datetime of the referred resource
     */
    readonly upload_datetime: string;
    /**
     * Resource type discriminator
     */
    resource_type: Submit.resource_type;
    /**
     * UUID resource unique identification
     */
    resource_id: string;
    readonly uploader: User;
};

export namespace Submit {
    /**
     * Resource type discriminator
     */
    export enum resource_type {
        BENCHMARK = 'benchmark',
        CLAIM = 'claim',
        SITE = 'site',
        FLAVOR = 'flavor',
    }
}

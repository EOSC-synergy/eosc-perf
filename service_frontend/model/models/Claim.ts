/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User } from './User';

export type Claim = {
    /**
     * Resource type discriminator
     */
    message: string;
    /**
     * Upload datetime of the referred resource
     */
    readonly upload_datetime: string;
    /**
     * UUID resource unique identification
     */
    readonly id: string;
    /**
     * Resource type discriminator
     */
    resource_type: Claim.resource_type;
    /**
     * UUID resource unique identification
     */
    readonly resource_id: string;
    readonly uploader: User;
};

export namespace Claim {
    /**
     * Resource type discriminator
     */
    export enum resource_type {
        RESULT = 'result',
    }
}

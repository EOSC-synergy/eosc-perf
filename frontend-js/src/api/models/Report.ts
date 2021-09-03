/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User } from './User';

export type Report = {
    /**
     * UUID resource unique identification
     */
    readonly id: string;
    /**
     * ISO8601 Datatime of the resource upload
     */
    upload_datetime: string;
    verdict: boolean;
    /**
     * Message included in a report
     */
    message: string;
    /**
     * Resource type discriminator
     */
    resource_type: Report.resource_type;
    /**
     * UUID resource unique identification
     */
    resource_id: string;
    readonly uploader: User;
}

export namespace Report {

    /**
     * Resource type discriminator
     */
    export enum resource_type {
        BENCHMARK = 'benchmark',
        RESULT = 'result',
        SITE = 'site',
        FLAVOR = 'flavor',
    }


}

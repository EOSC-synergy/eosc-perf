/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Report = {
    /**
     * UUID resource unique identification
     */
    readonly id: string;
    upload_date: string;
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

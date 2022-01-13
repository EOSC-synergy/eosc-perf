/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Flavor = {
    /**
     * String with virtual hardware template identification
     */
    name: string;
    /**
     * String with an statement about the object
     */
    description: string | null;
    /**
     * Upload datetime of the referred resource
     */
    readonly upload_datetime: string;
    /**
     * UUID resource unique identification
     */
    readonly id: string;
};

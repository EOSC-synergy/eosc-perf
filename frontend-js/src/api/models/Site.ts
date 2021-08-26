/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Site = {
    /**
     * UUID resource unique identification
     */
    readonly id: string;
    /**
     * String with human readable institution identification
     */
    name: string;
    /**
     * String with place where a site is located
     */
    address: string;
    /**
     * String with an statement about the object
     */
    description: string;
}

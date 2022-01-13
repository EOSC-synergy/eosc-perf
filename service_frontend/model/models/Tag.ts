/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Tag = {
    /**
     * String with short feature identification
     */
    name: string;
    /**
     * String with an statement about the object
     */
    description: string | null;
    /**
     * UUID resource unique identification
     */
    readonly id: string;
};

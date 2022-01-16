/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Benchmark = {
    /**
     * String with a docker hub container name
     */
    docker_image: string;
    /**
     * String with a docker hub container tag
     */
    docker_tag: string;
    json_schema: any;
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

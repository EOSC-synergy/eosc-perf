/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Benchmark = {
    /**
     * UUID resource unique identification
     */
    readonly id: string;
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
    description: string;
}
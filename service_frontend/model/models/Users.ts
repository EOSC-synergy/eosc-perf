/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User } from './User';

export type Users = {
    /**
     * True if a next page exists
     */
    readonly has_next: boolean;
    /**
     * True if a previous page exists
     */
    readonly has_prev: boolean;
    /**
     * Number of the next page
     */
    readonly next_num: number;
    /**
     * Number of the previous page
     */
    readonly prev_num: number;
    /**
     * The total number of pages
     */
    readonly pages: number;
    /**
     * The number of items to be displayed on a page
     */
    per_page: number;
    /**
     * The return page number (1 indexed)
     */
    page: number;
    /**
     * The total number of items matching the query
     */
    readonly total: number;
    items: Array<User>;
};

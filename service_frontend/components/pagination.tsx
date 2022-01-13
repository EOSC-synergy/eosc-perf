import React, { ReactElement } from 'react';
import { Pagination } from 'react-bootstrap';

/**
 * Representation of an OpenAPI pagination object
 */
export interface Paginatable {
    /**
     * Page index of next page
     */
    readonly next_num: number;

    /**
     * Page index of previous page
     */
    readonly prev_num: number;

    /**
     * Total number of pages
     */
    readonly total: number;

    /**
     * Maximum number of items per page
     */
    per_page?: number;

    /**
     * Whether there is a next page
     */
    readonly has_next: boolean;

    /**
     * Whether there is a previous page
     */
    readonly has_prev: boolean;

    /**
     * Total number of pages available
     */
    readonly pages: number;

    /**
     * The current page
     */
    page?: number;
}

/**
 * Generic for pagination of a specific object type
 */
export type Paginated<Type> = { items: Type[] } & Paginatable;

/**
 * Component to navigate between pages of a pagination object
 * @param {Paginatable} props.pagination paginatable object to navigate through
 * @param {(pageIndex: number) => void} props.navigateTo callback to navigate to another page in the pagination
 * @constructor
 */
export function Paginator(props: {
    pagination: Paginatable;
    navigateTo: (pageIndex: number) => void;
}): ReactElement {
    return (
        <Pagination className="align-items-center mb-0" data-testid="paginator">
            <Pagination.First
                disabled={props.pagination.pages === 0 || props.pagination.page === 1}
                onClick={() => props.navigateTo(1)}
                data-testid="paginator-first"
            />
            <Pagination.Prev
                disabled={!props.pagination.has_prev}
                onClick={() => props.navigateTo(props.pagination.prev_num)}
                data-testid="paginator-prev"
            />
            {/* TODO: don't show all pages, only nearby 3-5? */}
            {[...Array(props.pagination.pages).keys()].map((n: number) => (
                <Pagination.Item
                    active={props.pagination.page === n + 1}
                    onClick={() => props.navigateTo(n + 1)}
                    key={n + 1}
                >
                    {n + 1}
                </Pagination.Item>
            ))}
            <Pagination.Next
                disabled={!props.pagination.has_next}
                onClick={() => props.navigateTo(props.pagination.next_num)}
                data-testid="paginator-next"
            />
            <Pagination.Last
                disabled={
                    props.pagination.pages === 0 || props.pagination.page === props.pagination.pages
                }
                onClick={() => props.navigateTo(props.pagination.pages)}
                data-testid="paginator-last"
            />
        </Pagination>
    );
}

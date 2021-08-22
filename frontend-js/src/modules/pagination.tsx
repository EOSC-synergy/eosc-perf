/**
 * Page navigation based on flask pagination
 */

import { Pagination } from 'react-bootstrap';

export interface Paginatable {
    // index of next page
    readonly next_num: number;
    // index of previous page
    readonly prev_num: number;
    // total page count
    readonly total: number;
    // items per page
    per_page?: number;
    // whether there is a next page
    readonly has_next: boolean;
    // whether there is a previous page
    readonly has_prev: boolean;
    // number of pages
    readonly pages: number;
    // current page
    page?: number;
}

export function Paginator(props: {
    pagination: Paginatable;
    navigateTo: (pageIndex: number) => void;
}) {
    return (
        <Pagination>
            <Pagination.First
                disabled={props.pagination.page == 1}
                onClick={() => props.navigateTo(1)}
            />
            <Pagination.Prev
                disabled={!props.pagination.has_prev}
                onClick={() => props.navigateTo(props.pagination.prev_num)}
            />
            {/* TODO: don't show all pages, only nearby 3-5? */}
            {[...Array(props.pagination.pages).keys()].map((n: number) => (
                <Pagination.Item
                    disabled={props.pagination.page == n + 1}
                    onClick={() => props.navigateTo(n + 1)}
                >
                    {n + 1}
                </Pagination.Item>
            ))}
            <Pagination.Next
                disabled={!props.pagination.has_next}
                onClick={() => props.navigateTo(props.pagination.next_num)}
            />
            <Pagination.Last
                disabled={props.pagination.page == props.pagination.pages}
                onClick={() => props.navigateTo(props.pagination.pages)}
            />
        </Pagination>
    );
}

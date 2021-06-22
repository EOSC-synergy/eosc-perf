import { Pagination } from 'react-bootstrap';
import React from 'react';

export function NumberedPagination(props: {
    pageCount: number;
    currentPage: number;
    onChange: (newCount: number) => void;
}) {
    // don't display ellipsis if 6 pages or fewer
    if (props.pageCount < 6) {
        return (
            <Pagination>
                {[...Array(props.pageCount).keys()].map((pageIndex) => (
                    <Pagination.Item
                        key={pageIndex + 1}
                        active={props.currentPage === pageIndex}
                        onClick={(e) => props.onChange(pageIndex)}
                    >
                        {pageIndex + 1}
                    </Pagination.Item>
                ))}
            </Pagination>
        );
    }

    return <div>TODO: more than 6 pages</div>;
}
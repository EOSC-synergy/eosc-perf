import { Pagination } from 'react-bootstrap';
import React from 'react';

export function NumberedPagination(props: {
    pageCount: number;
    currentPage: number;
    onChange: (newCount: number) => void;
    className?: string;
}) {
    // don't display ellipsis if 6 pages or fewer
    if (props.pageCount < 6) {
        return (
            <nav aria-label="Page navigation" className={props.className}>
                {/* bottom margin forcibly removed */}
                <Pagination className="mb-0">
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
            </nav>
        );
    }

    return <div>TODO: more than 6 pages</div>;
}

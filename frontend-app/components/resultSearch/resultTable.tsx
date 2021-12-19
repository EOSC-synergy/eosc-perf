import React, { ReactElement, useState } from 'react';
import { Form, Table } from 'react-bootstrap';
import { Result } from 'model';
import {
    ActionColumn,
    BenchmarkColumn,
    CheckboxColumn,
    CustomColumn,
    SiteColumn,
    SiteFlavorColumn,
    TagsColumn
} from 'components/resultSearch/columns';
import { ResultOps } from 'components/resultSearch/resultOps';
import { ChevronDown, ChevronUp, Pencil } from 'react-bootstrap-icons';
import { ColumnSelectModal } from 'components/resultSearch/columnSelectModal';
import actionable from 'styles/actionable.module.css';
import { Ordered } from 'components/ordered';
import { Sorting, SortMode } from 'components/resultSearch/sorting';

function SortingTableHeader(props: {
    label: string;
    sortKey: string;
    sorting: Sorting;
    setSorting: (sort: Sorting) => void;
}) {
    function updateSortOrder() {
        if (props.sorting.key === props.sortKey) {
            // sort in reverse
            if (props.sorting.mode === SortMode.Ascending) {
                props.setSorting({ ...props.sorting, mode: SortMode.Descending });
            }
            // unsort
            else {
                props.setSorting({ mode: SortMode.Disabled, key: '' });
            }
        }
        // sorting by something else
        else {
            props.setSorting({ mode: SortMode.Ascending, key: props.sortKey });
        }
    }

    return (
        <th onClick={() => updateSortOrder()}>
            {props.label}{' '}
            {props.sorting.key === props.sortKey && (
                <>
                    {props.sorting.mode === SortMode.Ascending && <ChevronDown />}
                    {props.sorting.mode === SortMode.Descending && <ChevronUp />}
                </>
            )}
        </th>
    );
}

export function ResultTable(props: {
    results: Result[];
    pageOffset: number;
    ops: ResultOps;
    suggestions?: string[];
    sorting: Sorting;
    setSorting: (sort: Sorting) => void;
}): ReactElement {
    const [benchmarkColumnEnabled, setBenchmarkColumnEnabled] = useState(true);
    const [siteColumnEnabled, setSiteColumnEnabled] = useState(true);
    const [siteFlavorColumnEnabled, setSiteFlavorColumnEnabled] = useState(true);
    const [tagsColumnEnabled, setTagsColumnEnabled] = useState(true);

    const [customColumns, setCustomColumns] = useState<string[]>([]);

    // column selection modal
    const [showColumnSelection, setShowColumnSelection] = useState(false);

    return (
        <>
            <Table className='mb-0'>
                <thead>
                <tr>
                    <th>
                        <Form>
                            <Form.Check
                                type='switch'
                                onChange={() => {
                                    props.results.every((r) => props.ops.isSelected(r))
                                        ? props.ops.unselectMultiple(props.results)
                                        : props.ops.selectMultiple(
                                            props.results.map((r, i) => {
                                                return {
                                                    ...r,
                                                    orderIndex: i + props.pageOffset
                                                };
                                            })
                                        );
                                }}
                                checked={props.results.every((r) => props.ops.isSelected(r))}
                            />
                        </Form>
                    </th>
                    {benchmarkColumnEnabled && (
                        <SortingTableHeader
                            label='Benchmark'
                            sortKey='benchmark_name'
                            sorting={props.sorting}
                            setSorting={props.setSorting}
                        />
                    )}
                    {siteColumnEnabled && (
                        <SortingTableHeader
                            label='Site'
                            sortKey='site_name'
                            sorting={props.sorting}
                            setSorting={props.setSorting}
                        />
                    )}
                    {siteFlavorColumnEnabled && (
                        <SortingTableHeader
                            label='Site flavor'
                            sortKey='flavor_name'
                            sorting={props.sorting}
                            setSorting={props.setSorting}
                        />
                    )}
                    {tagsColumnEnabled && <th>Tags</th>}
                    {/* TODO: hover */}
                    {customColumns.map((column) => (
                        <th key={column}>{column}</th>
                    ))}
                    <th>
                        <a href='#' onClick={() => setShowColumnSelection(true)}>
                            <Pencil className={actionable.actionable} />
                        </a>
                    </th>
                </tr>
                </thead>

                <tbody>
                {props.results.map((result, index) => {
                    const r: Ordered<Result> = {
                        ...result,
                        orderIndex: index + props.pageOffset
                    };
                    return (
                        <tr key={r.id}>
                            <td>
                                <CheckboxColumn result={r} ops={props.ops} />
                            </td>
                            {benchmarkColumnEnabled && (
                                <td>
                                    <BenchmarkColumn result={r} />
                                </td>
                            )}
                            {siteColumnEnabled && (
                                <td>
                                    <SiteColumn result={r} />
                                </td>
                            )}
                            {siteFlavorColumnEnabled && (
                                <td>
                                    <SiteFlavorColumn result={r} />
                                </td>
                            )}
                            {tagsColumnEnabled && (
                                <td>
                                    <TagsColumn result={r} />
                                </td>
                            )}
                            {customColumns.map((column) => (
                                <td key={column}>
                                    <CustomColumn result={r} jsonKey={column} />
                                </td>
                            ))}
                            <td>
                                <ActionColumn result={r} ops={props.ops} />
                            </td>
                        </tr>
                    );
                })}
                </tbody>
            </Table>
            <ColumnSelectModal
                show={showColumnSelection}
                closeModal={() => setShowColumnSelection(false)}
                columns={customColumns}
                setColumns={setCustomColumns}
                suggestions={props.suggestions}
            />
        </>
    );
}

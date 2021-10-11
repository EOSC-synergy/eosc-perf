import React, { ReactElement, useState } from 'react';
import { Table } from 'react-bootstrap';
import { Result } from 'api';
import {
    ActionColumn,
    BenchmarkColumn,
    CheckboxColumn,
    CustomColumn,
    SiteColumn,
    SiteFlavorColumn,
    TagsColumn,
} from './columns';
import { ResultOps } from './resultOps';
import { Pencil } from 'react-bootstrap-icons';
import { ColumnSelectModal } from './columnSelectModal';
import '../../actionable.css';
import { Ordered } from 'components/ordered';

export function ResultTable(props: {
    results: Result[];
    pageOffset: number;
    ops: ResultOps;
    suggestions?: string[];
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
            <Table className="mb-0">
                <thead>
                    <tr>
                        {/* checkbox has no label */}
                        <th />
                        {benchmarkColumnEnabled && <th>Benchmark</th>}
                        {siteColumnEnabled && <th>Site</th>}
                        {siteFlavorColumnEnabled && <th>Site flavor</th>}
                        {tagsColumnEnabled && <th>Tags</th>}
                        {/* TODO: hover */}
                        {customColumns.map((column) => (
                            <th key={column}>{column}</th>
                        ))}
                        <th>
                            <a href="#" onClick={() => setShowColumnSelection(true)}>
                                <Pencil className="actionable" />
                            </a>
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {props.results.map((result, index) => {
                        const r: Ordered<Result> = {
                            ...result,
                            orderIndex: index + props.pageOffset,
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
            />
        </>
    );
}

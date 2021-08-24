import { Form, Table } from 'react-bootstrap';
import { Result } from '../../api';
import {
    CheckboxColumn,
    BenchmarkColumn,
    SiteColumn,
    SiteFlavorColumn,
    TagsColumn,
    ActionColumn,
    CustomColumn,
} from './columns';
import { useState } from 'react';
import { ResultOps } from './resultOps';
import { Pencil } from 'react-bootstrap-icons';
import { ColumnSelectModal } from './columnSelectModal';
import '../../actionable.css';

export function ResultTable(props: {
    results: Result[];
    customColumns: string[];
    ops: ResultOps;
    admin: boolean;
}) {
    const [benchmarkColumnEnabled, setBenchmarkColumnEnabled] = useState(true);
    const [siteColumnEnabled, setSiteColumnEnabled] = useState(true);
    const [siteFlavorColumnEnabled, setSiteFlavorColumnEnabled] = useState(true);
    const [tagsColumnEnabled, setTagsColumnEnabled] = useState(true);

    const [customColumns, setCustomColumns] = useState<string[]>([]);

    // column selection modal
    const [showColumnSelection, setShowColumnSelection] = useState(false);

    return (
        <>
            <Table>
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
                            <a onClick={() => setShowColumnSelection(true)}>
                                <Pencil className="actionable" />
                            </a>
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {props.results.map((result) => (
                        <tr key={result.id}>
                            <td>
                                <CheckboxColumn result={result} ops={props.ops} />
                            </td>
                            {benchmarkColumnEnabled && (
                                <td>
                                    <BenchmarkColumn result={result} />
                                </td>
                            )}
                            {siteColumnEnabled && (
                                <td>
                                    <SiteColumn result={result} />
                                </td>
                            )}
                            {siteFlavorColumnEnabled && (
                                <td>
                                    <SiteFlavorColumn result={result} />
                                </td>
                            )}
                            {tagsColumnEnabled && (
                                <td>
                                    <TagsColumn result={result} />
                                </td>
                            )}
                            {customColumns.map((column) => (
                                <td key={column}>
                                    <CustomColumn result={result} jsonKey={column} />
                                </td>
                            ))}
                            <td>
                                <ActionColumn result={result} ops={props.ops} admin={props.admin} />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <ColumnSelectModal
                show={showColumnSelection}
                closeModal={() => setShowColumnSelection(false)}
                columns={[] /* TODO */}
            />
        </>
    );
}

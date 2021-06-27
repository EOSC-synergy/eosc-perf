import { Table } from 'react-bootstrap';
import { Column } from './column';
import { SelectableResult } from './selectableResult';

export function ResultTable(props: { results: SelectableResult[]; columns: Column[] }) {
    return (
        <Table style={{ overflowX: 'auto', display: 'inline-block' }} className="m-2">
            <thead>
                <tr>
                    {props.columns.map((column) => (
                        <th key={column.name}>{column.name}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {props.results.map((result) => (
                    <tr key={result.id}>
                        {props.columns.map((column) => (
                            <td>{column.generateView(result)}</td>
                        ))}
                    </tr>
                ))}
            </tbody>
            {props.results.length === 0 && 'No results found! :('}
        </Table>
    );
}

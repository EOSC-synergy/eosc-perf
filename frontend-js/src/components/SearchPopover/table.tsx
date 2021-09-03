import { ReactNode } from 'react';
import { Identifiable } from '../identifiable';

export function Table<Item extends Identifiable>(props: {
    items?: Item[];
    setItem: (benchmark: Item) => void;
    tableName: string;
    displayItem: (item: Item) => ReactNode;
}) {
    return (
        <table style={{ width: '100%' }}>
            <thead>
                <tr>
                    <th style={{ borderBottom: '3px solid #000' }}>{props.tableName}</th>
                </tr>
            </thead>
            <tbody>
                {props.items && props.items.length > 0 ? (
                    props.items.map((item: Item) => (
                        <tr key={item.id}>
                            <td style={{ borderBottom: '1px solid #ddd' }}>
                                {props.displayItem(item)}
                            </td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td>No results found!</td>
                    </tr>
                )}
            </tbody>
        </table>
    );
}
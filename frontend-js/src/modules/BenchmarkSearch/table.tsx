import { Result } from './types';
import React from 'react';

type TableProps = {
    results: Result[];
};

export function Table(props: { results: Result[] }) {
    return (
        <table>
            <thead>
                <tr>
                    <th>Benchmarks</th>
                </tr>
            </thead>
            <tbody>
                {props.results.map((result: Result) => (
                    <tr>
                        <td>
                            {result.dockerImage + ':' + result.dockerTag}
                            <div> {result.description} </div>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}

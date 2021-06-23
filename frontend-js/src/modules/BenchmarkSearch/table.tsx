import { Result } from './types';
import React from 'react';

type TableProps = {
    results: Result[];
};

export function Table(props: TableProps) {
    return (
        <table>
            <thead>
                <tr>
                    <th>Benchmarks</th>
                </tr>
            </thead>
            <tbody>
                {props.results.length > 0 ? (
                    props.results.map((result: Result) => (
                        <tr>
                            <td>
                                {/* TODO: link to result search module with query strings */}
                                {result.dockerImage + ':' + result.dockerTag}
                                <div> {result.description} </div>
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

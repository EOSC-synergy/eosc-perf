import React from 'react';
import { Benchmark } from '../../api';

type TableProps = {
    results: Benchmark[];
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
                    props.results.map((result: Benchmark) => (
                        <tr>
                            <td>
                                {/* TODO: link to result search module with query strings */}
                                {result.docker_image + ':' + result.docker_tag}
                                <div> {/*result.description*/} </div>
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

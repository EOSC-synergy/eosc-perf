import React from 'react';
import { Benchmark } from '../../api';

import modules from '..';

type TableProps = {
    results: Benchmark[];
};

export function Table(props: TableProps) {
    return (
        <table style={{ width: '100%' }}>
            <thead>
                <tr>
                    <th style={{ borderBottom: '3px solid #000' }}>Benchmarks</th>
                </tr>
            </thead>
            <tbody>
                {props.results.length > 0 ? (
                    props.results.map((result: Benchmark) => (
                        <tr>
                            <td style={{ borderBottom: '1px solid #ddd' }}>
                                <a
                                    href={modules.ResultSearch.path + '?benchmark=' + result.id}
                                    title={result.docker_image + ':' + result.docker_tag}
                                >
                                    {result.docker_image + ':' + result.docker_tag}
                                </a>
                                <div>
                                    {result.description}
                                    <br />
                                </div>
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

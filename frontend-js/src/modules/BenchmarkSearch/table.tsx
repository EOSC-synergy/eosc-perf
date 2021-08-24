import React from 'react';
import { Benchmark } from '../../api';

import modules from '..';

export function Table(props: { results?: Benchmark[] }) {
    return (
        <table style={{ width: '100%' }}>
            <thead>
                <tr>
                    <th style={{ borderBottom: '3px solid #000' }}>Benchmarks</th>
                </tr>
            </thead>
            <tbody>
                {props.results ? (
                    props.results.map((benchmark: Benchmark) => (
                        <tr key={benchmark.id}>
                            <td style={{ borderBottom: '1px solid #ddd' }}>
                                <a
                                    href={modules.ResultSearch.path + '?benchmark=' + benchmark.id}
                                    title={benchmark.docker_image + ':' + benchmark.docker_tag}
                                >
                                    {benchmark.docker_image + ':' + benchmark.docker_tag}
                                </a>
                                <div>
                                    {benchmark.description}
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

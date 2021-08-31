import { useQuery } from 'react-query';
import { getHelper } from '../../api-helpers';
import { Benchmarks } from '../../api';
import { Card, Form, Popover } from 'react-bootstrap';
import React from 'react';

export function BenchmarkSelection(props: {
    benchmark?: string;
    setBenchmark: (benchmark: string) => void;
}) {
    let benchmarks = useQuery(
        'benchmarks',
        () => {
            return getHelper<Benchmarks>('/benchmarks');
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <>
            <Form.Group>
                <Form.Label>Select benchmark:</Form.Label>
                <Form.Control
                    as="select"
                    value={props.benchmark}
                    onChange={(e) => props.setBenchmark(e.target.value)}
                >
                    {benchmarks.isSuccess &&
                        benchmarks.data.data.items!.map((benchmark) => (
                            <option value={benchmark.id} key={benchmark.id}>
                                {benchmark.docker_image}:{benchmark.docker_tag}
                            </option>
                        ))}
                </Form.Control>
            </Form.Group>
        </>
    );
}

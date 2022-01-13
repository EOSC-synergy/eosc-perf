import { Ordered } from '../../ordered';
import { Result, Site } from '../../../model';
import { fetchSubkey } from '../jsonKeyHelpers';
import { Suggestion } from '../jsonSchema';
import { Form } from 'react-bootstrap';
import { InputWithSuggestions } from '../../inputWithSuggestions';
import React from 'react';

export type DataPoint = { x: number; y: number; result: Ordered<Result> };
export type DataPointCollection = Map<string, { site: Site; data: DataPoint[] }>;
export type RejectedResult = { result: Ordered<Result>; reason: string };

export function generateDataPoints(
    results: Ordered<Result>[],
    xAxis: string,
    yAxis: string
): [DataPointCollection, RejectedResult[]] {
    let rejected: { result: Ordered<Result>; reason: string }[] = [];
    const collection: DataPointCollection = new Map<string, { site: Site; data: DataPoint[] }>();

    for (const result of results) {
        const x = fetchSubkey(result.json, xAxis);
        const y = fetchSubkey(result.json, yAxis);

        if (typeof fetchSubkey(result.json, xAxis) !== 'number') {
            rejected.push({ result, reason: 'X axis value not numeric' });
            continue;
        }
        if (typeof fetchSubkey(result.json, yAxis) !== 'number') {
            rejected.push({ result, reason: 'Y axis value not numeric' });
            continue;
        }
        if (collection.get(result.site.id) === undefined) {
            collection.set(result.site.id, {
                site: result.site,
                data: [],
            });
        }
        collection.get(result.site.id)?.data.push({ x: x as number, y: y as number, result });
    }

    // sort them left to right
    for (const entry of collection.values()) {
        entry.data.sort((a: DataPoint, b: DataPoint) => a.x - b.x);
    }

    return [collection, rejected];
}

export function XAxis(props: {
    setXAxis: (value: ((prevState: string) => string) | string) => void;
    suggestions?: Suggestion[];
}) {
    return (
        <Form.Group className="mb-1">
            <Form.Label>X Axis:</Form.Label>
            <InputWithSuggestions
                placeholder="machine.cpu.count"
                setInput={(i) => props.setXAxis(i)}
                suggestions={props.suggestions}
            />
        </Form.Group>
    );
}

export function YAxis(props: {
    setYAxis: (value: ((prevState: string) => string) | string) => void;
    suggestions?: Suggestion[];
}) {
    return (
        <Form.Group>
            <Form.Label>Y Axis:</Form.Label>
            <InputWithSuggestions
                placeholder="result.score"
                setInput={(i) => props.setYAxis(i)}
                suggestions={props.suggestions}
            />
        </Form.Group>
    );
}

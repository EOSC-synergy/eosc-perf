import React, { ChangeEvent, ReactElement, useState } from 'react';
import { Benchmark, Result } from 'model';
import { Badge, Form } from 'react-bootstrap';
import charts from 'components/resultSearch/diagrams';
import { Ordered } from 'components/ordered';
import { Suggestion } from './jsonSchema';

export function DiagramView(props: {
    results: Ordered<Result>[];
    benchmark?: Benchmark;
    suggestions?: Suggestion[];
}): ReactElement {
    const [selectedDiagram, setSelectedDiagram] = useState(charts.LineChartMeta.id);

    return (
        <>
            <Form.Group className="mb-1">
                <Form.Label htmlFor="diagramDropdown">Select diagram type:</Form.Label>{' '}
                {props.benchmark === undefined && (
                    <Badge bg="danger">Please select a benchmark first</Badge>
                )}
                <Form.Select
                    onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                        setSelectedDiagram(e.target.value);
                    }}
                    className="custom-select"
                    disabled={props.benchmark === undefined}
                >
                    {charts.all.map((chart) => (
                        <option value={chart.id} key={chart.id}>
                            {chart.name}
                        </option>
                    ))}
                </Form.Select>
            </Form.Group>
            {props.benchmark !== undefined &&
                charts.all.map((chart) => (
                    <div key={chart.id}>
                        {chart.id === selectedDiagram && (
                            <chart.element
                                results={props.results}
                                benchmark={props.benchmark}
                                suggestions={props.suggestions}
                            />
                        )}
                    </div>
                ))}
        </>
    );
}

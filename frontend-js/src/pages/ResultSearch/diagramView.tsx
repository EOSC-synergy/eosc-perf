import React, { ReactElement, useState } from 'react';
import { Benchmark, Result } from 'api';
import { Badge, Form } from 'react-bootstrap';
import charts from './diagrams';

export function DiagramView(props: {
    results: Result[];
    benchmark?: Benchmark;
    suggestions?: string[];
}): ReactElement {
    const [selectedDiagram, setSelectedDiagram] = useState(charts.LineChartMeta.id);

    return (
        <>
            <Form.Group>
                <Form.Label htmlFor="diagramDropdown">Select diagram type:</Form.Label>{' '}
                {props.benchmark === undefined && (
                    <Badge bg="danger">Please select a benchmark first</Badge>
                )}
                <Form.Control
                    as="select"
                    onChange={(e) => {
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
                </Form.Control>
            </Form.Group>
            {props.benchmark !== undefined &&
                charts.all.map((chart) => (
                    <div key={chart.id}>
                        {chart.id === selectedDiagram && (
                            <chart.element results={props.results} benchmark={props.benchmark} />
                        )}
                    </div>
                ))}
        </>
    );
}

import { Benchmark, Result } from '../../api';
import { Badge, Form } from 'react-bootstrap';
import charts from './diagrams';
import React, { useState } from 'react';

export function DiagramView(props: {
    results: Result[];
    benchmark?: Benchmark;
    suggestions?: string[];
}) {
    const [selectedDiagram, setSelectedDiagram] = useState(charts.LineChartMeta.id);

    return (
        <>
            <Form.Group>
                <label htmlFor="diagramDropdown">Select diagram type:</label>
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
                {props.benchmark === undefined && (
                    <Badge bg="danger">Please select a benchmark</Badge>
                )}
            </Form.Group>
            {props.benchmark !== undefined &&
                charts.all.map((chart) => (
                    <div key={chart.id}>
                        {chart.id == selectedDiagram && (
                            // @ts-ignore
                            <chart.element results={props.results} benchmark={props.benchmark} />
                        )}
                    </div>
                ))}
        </>
    );
}

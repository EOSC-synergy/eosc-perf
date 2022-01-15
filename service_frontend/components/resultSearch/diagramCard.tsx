import React, { ChangeEvent, ReactElement, useState } from 'react';
import { Benchmark, Result } from 'model';
import { Badge, Card, Col, Form, Row } from 'react-bootstrap';
import charts from 'components/resultSearch/diagrams';
import { Ordered } from 'components/ordered';
import { Suggestion } from './jsonSchema';

export function DiagramCard(props: {
    results: Ordered<Result>[];
    benchmark?: Benchmark;
    suggestions?: Suggestion[];
}): ReactElement {
    const [selectedDiagram, setSelectedDiagram] = useState(charts.EChartsMeta.id);

    return (
        <>
            <Card>
                <Card.Header>
                    <Row>
                        <Form.Group>
                            <Row>
                                <Col className="align-self-center">
                                    <Form.Label style={{ marginBottom: 0 }}>Diagram</Form.Label>
                                </Col>
                                <Col md="auto">
                                    {props.benchmark !== undefined && (
                                        <Form.Select
                                            onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                                                setSelectedDiagram(e.target.value);
                                            }}
                                            className="custom-select"
                                            size="sm"
                                            value={selectedDiagram}
                                        >
                                            <option>None</option>
                                            {charts.all.map((chart) => (
                                                <option value={chart.id} key={chart.id}>
                                                    {chart.name}
                                                </option>
                                            ))}
                                        </Form.Select>
                                    )}
                                    {props.benchmark === undefined && (
                                        <Badge bg="danger">Please select a benchmark</Badge>
                                    )}
                                </Col>
                            </Row>
                        </Form.Group>
                    </Row>
                </Card.Header>
                {props.benchmark !== undefined && (
                    <Card.Body>
                        {charts.all.map((chart) => (
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
                    </Card.Body>
                )}
            </Card>
        </>
    );
}

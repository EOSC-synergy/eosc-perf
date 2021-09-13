import React, { ChangeEvent } from 'react';
import { Col, Form, Row } from 'react-bootstrap';

export function ResultsPerPageSelection(props: {
    onChange: (resultsPerPage: number) => void;
    currentSelection: number;
}) {
    const options = [10, 15, 20, 50, 100];

    return (
        <Form.Group as={Row}>
            <Form.Label column>Results per page:</Form.Label>
            <Col>
                <Form.Select
                    onChange={(e: ChangeEvent<HTMLSelectElement>) =>
                        props.onChange(parseInt(e.target.value))
                    }
                    value={props.currentSelection}
                >
                    {options.map((n: number) => (
                        <option value={n.toString()} key={n.toString()}>
                            {n.toString()}
                        </option>
                    ))}
                </Form.Select>
            </Col>
        </Form.Group>
    );
}

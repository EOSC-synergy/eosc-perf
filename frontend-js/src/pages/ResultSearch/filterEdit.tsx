import { Filter } from 'pages/ResultSearch/filter';
import React, { ChangeEvent, useState } from 'react';
import { CloseButton, Col, Form, InputGroup, Row } from 'react-bootstrap';

export function FilterEdit(props: {
    filter: Filter;
    setFilter: (id: string, key: string, mode: string, value: string) => void;
    deleteFilter: (id: string) => void;
}) {
    const [key, setKey] = useState(props.filter.key);
    const [mode, setMode] = useState(props.filter.mode);
    const [value, setValue] = useState(props.filter.value);

    return (
        <Row>
            <Col>
                <InputGroup>
                    <Form.Control
                        aria-label="JSON Key"
                        placeholder="JSON Key"
                        value={key}
                        onChange={(e) => {
                            setKey(e.target.value);
                            props.setFilter(props.filter.id, e.target.value, mode, value);
                        }}
                    />
                    <Form.Select
                        value={mode}
                        onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                            // TODO: why do they say it's a FormEvent and we have to assert ChangeEvent??
                            setMode(e.target.value);
                            props.setFilter(props.filter.id, key, mode, value);
                        }}
                    >
                        <option value=">">&gt;</option>
                        <option value=">=">≥</option>
                        <option value="==">=</option>
                        <option value="<=">≤</option>
                        <option value="<">&lt;</option>
                    </Form.Select>
                    <Form.Control
                        aria-label="Value"
                        placeholder="Value"
                        value={value}
                        onChange={(e) => {
                            setValue(e.target.value);
                            props.setFilter(props.filter.id, key, mode, e.target.value);
                        }}
                    />
                </InputGroup>
            </Col>
            <Col md="auto">
                <CloseButton onClick={() => props.deleteFilter(props.filter.id)} />
            </Col>
        </Row>
    );
}

import React, { ChangeEvent, ReactElement, useState } from 'react';
import { Filter } from 'components/resultSearch/filter';
import { CloseButton, Col, Form, Row } from 'react-bootstrap';
import { InputWithSuggestions } from 'components/inputWithSuggestions';
import { Suggestion } from './jsonSchema';

export function FilterEdit(props: {
    filter: Filter;
    setFilter: (id: string, key: string, mode: string, value: string) => void;
    deleteFilter: (id: string) => void;
    suggestions?: Suggestion[];
}): ReactElement {
    const [key, setKey] = useState(props.filter.key);
    const [mode, setMode] = useState(props.filter.mode);
    const [value, setValue] = useState(props.filter.value);

    return (
        <Row>
            <Col>
                <InputWithSuggestions
                    suggestions={props.suggestions}
                    setInput={(e) => {
                        setKey(e);
                        props.setFilter(props.filter.id, e, mode, value);
                    }}
                    placeholder="JSON Key"
                >
                    <Form.Select
                        value={mode}
                        onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                            // TODO: why do they say it's a FormEvent and we have to assert ChangeEvent??
                            setMode(e.target.value);
                            props.setFilter(props.filter.id, key, e.target.value, value);
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
                </InputWithSuggestions>
            </Col>
            <Col md="auto">
                <CloseButton onClick={() => props.deleteFilter(props.filter.id)} />
            </Col>
        </Row>
    );
}

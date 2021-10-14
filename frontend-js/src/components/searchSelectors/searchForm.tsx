import React, { ReactElement, useState } from 'react';
import { Button, Col, Form, Row } from 'react-bootstrap';

export function SearchForm(props: { setSearchString: (params: string) => void }): ReactElement {
    const [message, setMessage] = useState('');

    return (
        <Form>
            <Form.Group as={Row}>
                <Form.Label className="visually-hidden" column>
                    Query
                </Form.Label>
                <Col>
                    <Form.Control
                        type="text"
                        placeholder="Enter your query here, keywords separated by spaces"
                        onChange={(e) => setMessage(e.target.value)}
                    />
                </Col>
                <Col md="auto">
                    <Button variant="info" onClick={() => props.setSearchString(message)}>
                        Search
                    </Button>
                </Col>
            </Form.Group>
        </Form>
    );
}

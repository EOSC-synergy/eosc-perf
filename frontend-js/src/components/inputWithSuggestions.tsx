import React, { ReactElement, ReactNode, useState } from 'react';
import { Dropdown, FormControl, InputGroup } from 'react-bootstrap';

export function InputWithSuggestions(props: {
    setInput: (input: string) => void;
    suggestions?: string[];
    placeholder?: string;
    children?: ReactNode;
}): ReactElement {
    const [input, setInput] = useState('');

    return (
        <Dropdown
            as={InputGroup}
            onSelect={(k) => {
                setInput(k ?? '');
                props.setInput(k ?? '');
            }}
        >
            <FormControl
                placeholder={props.placeholder}
                aria-label={props.placeholder ?? 'Input field with suggestions'}
                value={input}
            />
            {props.suggestions !== undefined && props.suggestions.length > 0 && (
                <>
                    <Dropdown.Toggle split variant="outline-secondary" />
                    <Dropdown.Menu>
                        {props.suggestions.map((suggestion) => (
                            <Dropdown.Item key={suggestion} eventKey={suggestion}>
                                {suggestion}
                            </Dropdown.Item>
                        ))}
                    </Dropdown.Menu>
                </>
            )}
            {/* TODO: clean up, find alternative for this (this is used in filters) */}
            {props.children}
        </Dropdown>
    );
}

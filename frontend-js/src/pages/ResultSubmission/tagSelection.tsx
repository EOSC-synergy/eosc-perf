import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';
import { Tags } from 'api';
import React, { useState } from 'react';
import { Button, Form, InputGroup, ListGroup } from 'react-bootstrap';

export function TagSelection(props: {
    tags: string[];
    addTag: (tag: string) => void;
    removeTag: (tag: string) => void;
}) {
    let tags = useQuery(
        'tags',
        () => {
            return getHelper<Tags>('/tags');
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    const [customTagName, setCustomTagName] = useState('');

    function addCustomTag() {}

    return (
        <>
            <Form.Group>
                <Form.Label>Select tags:</Form.Label>
                <div className="scrollable-dropdown">
                    <ListGroup>
                        {/* TODO: make this look nicer? */}
                        {tags.isSuccess &&
                            (tags.data.data.items!.length > 0 ? (
                                tags.data.data.items!.map((t) =>
                                    props.tags.includes(t.id) ? (
                                        <ListGroup.Item onClick={() => props.removeTag(t.id!)}>
                                            {t.name}
                                        </ListGroup.Item>
                                    ) : (
                                        <ListGroup.Item onClick={() => props.addTag(t.id!)}>
                                            {t.name}
                                        </ListGroup.Item>
                                    )
                                )
                            ) : (
                                <ListGroup.Item disabled>No tags available.</ListGroup.Item>
                            ))}
                    </ListGroup>
                </div>
            </Form.Group>
            <Form.Group>
                <Form.Label htmlFor="custom-tag">Custom tag</Form.Label>
                <InputGroup>
                    <Form.Control
                        id="custom-tag"
                        placeholder="tensor"
                        onChange={(e) => setCustomTagName(e.target.value)}
                    />
                    <Button
                        variant="success"
                        disabled={customTagName.length < 1}
                        onClick={addCustomTag}
                    >
                        Add Tag
                    </Button>
                </InputGroup>
            </Form.Group>
        </>
    );
}

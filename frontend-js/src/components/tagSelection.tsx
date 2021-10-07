import React, { ReactElement, useContext, useState } from 'react';
import { useMutation, useQuery } from 'react-query';
import { getHelper, postHelper } from 'api-helpers';
import { CreateTag, Tags } from 'api';
import { Button, Form, InputGroup, ListGroup } from 'react-bootstrap';
import { UserContext } from 'userContext';

export function TagSelection(props: {
    tags: string[];
    addTag: (tag: string) => void;
    removeTag: (tag: string) => void;
}): ReactElement {
    const tags = useQuery(
        'tags',
        () => {
            return getHelper<Tags>('/tags');
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    const auth = useContext(UserContext);

    const { mutate } = useMutation(
        (data: CreateTag) => postHelper<CreateTag>('/tags', data, auth.token),
        {
            onSuccess: () => {
                tags.refetch().then(() => undefined);
            },
        }
    );

    function addTag() {
        mutate({
            name: customTagName,
            description: '',
        });
    }

    const [customTagName, setCustomTagName] = useState('');

    return (
        <>
            <Form.Group className="mb-3">
                <Form.Label>Select tags:</Form.Label>
                <div className="scrollable-dropdown">
                    <ListGroup>
                        {/* TODO: make this look nicer? */}
                        {/* Not using <ListGroup.Item action> as it adds behaviour */}
                        {tags.isSuccess &&
                            (tags.data.data.items.length > 0 ? (
                                tags.data.data.items.map((t) =>
                                    props.tags.includes(t.id) ? (
                                        <ListGroup.Item
                                            onClick={() => props.removeTag(t.id)}
                                            key={t.id}
                                            className="list-group-item-action"
                                            active
                                        >
                                            {t.name}
                                        </ListGroup.Item>
                                    ) : (
                                        <ListGroup.Item
                                            onClick={() => props.addTag(t.id)}
                                            key={t.id}
                                            className="list-group-item-action"
                                            action
                                        >
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
                        disabled={!auth.token || customTagName.length < 1}
                        onClick={() => addTag()}
                    >
                        Add Tag
                    </Button>
                </InputGroup>
            </Form.Group>
        </>
    );
}

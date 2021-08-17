import { Flavor, FlavorEdit } from '../../api';
import React, { useState } from 'react';
import { useMutation } from 'react-query';
import { putHelper } from '../../api-helpers';
import { Button, Form, InputGroup, ListGroup } from 'react-bootstrap';
import { Check, PencilSquare } from 'react-bootstrap-icons';

export function FlavorEditor(props: { flavor: Flavor; token: string; refetch: () => void }) {
    const [name, setName] = useState(props.flavor.name);
    const [desc, setDesc] = useState(props.flavor.description);

    const [editing, setEditing] = useState(false);

    function updateEditing(editing: boolean) {
        if (editing) {
            setName(props.flavor.name);
            setDesc(props.flavor.description);
        }
        setEditing(editing);
    }

    const { mutate, isLoading } = useMutation(
        (data: FlavorEdit) =>
            putHelper<FlavorEdit>('/sites/flavors/' + props.flavor.id, data, props.token, {
                flavor_id: props.flavor.id,
            }),
        {
            onSuccess: (data) => {
                setEditing(false);
                props.refetch();
            },
        }
    );

    return (
        <ListGroup.Item key={props.flavor.id} id={props.flavor.id}>
            <InputGroup>
                <Form.Control
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    readOnly={!editing}
                />
                <Button
                    onClick={() => {
                        mutate({ name, description: desc });
                    }}
                    disabled={!editing}
                >
                    <Check />
                </Button>
                <Button onClick={() => updateEditing(!editing)}>
                    <PencilSquare />
                </Button>
            </InputGroup>
            <Form.Control
                as="textarea"
                onChange={(e) => setDesc(e.target.value)}
                readOnly={!editing}
                value={desc}
            />
        </ListGroup.Item>
    );
}

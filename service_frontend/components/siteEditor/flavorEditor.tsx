import { Flavor } from 'model';
import React, { ReactElement, useContext, useState } from 'react';
import { useMutation } from 'react-query';
import { putHelper } from 'components/api-helpers';
import { Button, Form, InputGroup, ListGroup } from 'react-bootstrap';
import { Check, PencilSquare } from 'react-bootstrap-icons';
import { UserContext } from 'components/userContext';

export function FlavorEditor(props: { flavor: Flavor; refetch: () => void }): ReactElement {
    const [name, setName] = useState<string>(props.flavor.name);
    const [desc, setDesc] = useState<string>(
        props.flavor.description ? props.flavor.description : ''
    );

    const [editing, setEditing] = useState(false);

    const auth = useContext(UserContext);

    function updateEditing(editing: boolean) {
        if (editing) {
            setName(props.flavor.name);
            setDesc(props.flavor.description ? props.flavor.description : '');
        }
        setEditing(editing);
    }

    const { mutate } = useMutation(
        (data: Flavor) =>
            putHelper<Flavor>('/sites/flavors/' + props.flavor.id, data, auth.token, {
                flavor_id: props.flavor.id,
            }),
        {
            onSuccess: () => {
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
                        mutate({
                            name,
                            description: desc.length ? desc : null,
                            id: props.flavor.id,
                            upload_datetime: props.flavor.upload_datetime,
                        });
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

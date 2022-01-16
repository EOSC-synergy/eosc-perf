import { Site } from 'model';
import { Form } from 'react-bootstrap';
import React, { ReactElement, useState } from 'react';

export function SiteId(props: { site: Site }): ReactElement {
    return (
        <Form.Group className="mb-3">
            <Form.Label>Identifier:</Form.Label>
            <Form.Control type="text" value={props.site.id} readOnly />
        </Form.Group>
    );
}

export function SiteName(props: { site: Site; update: (newName: string) => void }): ReactElement {
    const [name, setName] = useState(props.site.name);

    return (
        <Form.Group className="mb-3">
            <Form.Label>Name:</Form.Label>
            <Form.Control
                onChange={(e) => {
                    setName(e.target.value);
                    props.update(e.target.value);
                }}
                value={name}
                readOnly={false}
            />
        </Form.Group>
    );
}

export function Description(props: {
    site: Site;
    update: (description: string) => void;
}): ReactElement {
    const [description, setDescription] = useState<string>(
        props.site.description ? props.site.description : ''
    );

    return (
        <Form.Group className="mb-3">
            <Form.Label>Description:</Form.Label>
            <Form.Control
                as="textarea"
                onChange={(e) => {
                    setDescription(e.target.value);
                    props.update(e.target.value);
                }}
                value={description}
            />
        </Form.Group>
    );
}

export function NetAddress(props: { site: Site; update: (address: string) => void }): ReactElement {
    const [address, setAddress] = useState(props.site.address);

    return (
        <Form.Group className="mb-3">
            <Form.Label>Network address:</Form.Label>
            <Form.Control
                onChange={(e) => {
                    setAddress(e.target.value);
                    props.update(e.target.value);
                }}
                value={address}
            />
        </Form.Group>
    );
}

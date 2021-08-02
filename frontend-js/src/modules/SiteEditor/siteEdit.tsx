import { Site } from '../../api';
import { useMutation } from 'react-query';
import { putHelper } from '../../api-helpers';
import React, { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import { Description, NetAddress, SiteId, SiteName } from './siteFields';
import { FlavorList } from './flavorList';

export function SiteEdit(props: { token: string; site: Site; refetch: () => void }) {
    const { mutate, isLoading } = useMutation(
        (data: Site) =>
            putHelper<Site>('/sites/' + props.site.id, data, props.token, {
                site_id: props.site.id,
            }),
        {
            onSuccess: () => {
                props.refetch();
            },
        }
    );

    const [name, setName] = useState(props.site.name);
    const [description, setDescription] = useState(props.site.description);
    const [address, setAddress] = useState(props.site.address);

    return (
        <Form>
            <SiteId site={props.site} />
            <SiteName site={props.site} update={(name: string) => setName(name)} />
            <Description
                site={props.site}
                update={(description: string) => setDescription(description)}
            />
            <NetAddress site={props.site} update={(address: string) => setAddress(address)} />
            <Button
                variant="success"
                onClick={() => {
                    mutate({ name, description, address });
                }}
            >
                Submit
            </Button>
            <FlavorList site={props.site} token={props.token} />
        </Form>
    );
}

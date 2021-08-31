import { Site, SiteEdit } from '../../api';
import { useMutation } from 'react-query';
import { putHelper } from '../../api-helpers';
import React, { useContext, useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import { Description, NetAddress, SiteId, SiteName } from './siteFields';
import { FlavorList } from './flavorList';
import { UserContext } from '../../userContext';

export function SiteEditor(props: { site: Site; refetch: () => void }) {
    const auth = useContext(UserContext);

    const { mutate, isLoading } = useMutation(
        (data: SiteEdit) =>
            putHelper<SiteEdit>('/sites/' + props.site.id, data, auth.token, {
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
            <FlavorList site={props.site} />
        </Form>
    );
}

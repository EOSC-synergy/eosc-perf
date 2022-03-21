import { Site } from 'api';
import { useMutation } from 'react-query';
import { putHelper } from 'api-helpers';
import React, { ReactElement, useContext, useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import { Description, NetAddress, SiteId, SiteName } from 'components/siteEditor/siteFields';
import { FlavorList } from 'components/siteEditor/flavorList';
import { UserContext } from 'components/userContext';

export function SiteEditor(props: { site: Site; refetch: () => void }): ReactElement {
    const auth = useContext(UserContext);

    const { mutate } = useMutation(
        (data: Site) =>
            putHelper<Site>('/sites/' + props.site.id, data, auth.token, {
                site_id: props.site.id,
            }),
        {
            onSuccess: () => {
                props.refetch();
            },
        }
    );

    const [name, setName] = useState(props.site.name);
    const [description, setDescription] = useState<string>(
        props.site.description ? props.site.description : ''
    );
    const [address, setAddress] = useState(props.site.address);

    return (
        <Form>
            <Form.Group className="mb-3">
                <SiteId site={props.site} />
            </Form.Group>
            <Form.Group className="mb-3">
                <SiteName site={props.site} update={(name: string) => setName(name)} />
            </Form.Group>
            <Form.Group className="mb-3">
                <Description
                    site={props.site}
                    update={(description: string) => setDescription(description)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <NetAddress site={props.site} update={(address: string) => setAddress(address)} />
            </Form.Group>
            <Form.Group className="mb-3">
                <Button
                    variant="success"
                    onClick={() => {
                        mutate({
                            name,
                            description: description.length ? description : null,
                            address,
                            id: props.site.id,
                            upload_datetime: props.site.upload_datetime,
                        });
                    }}
                >
                    Submit
                </Button>
            </Form.Group>
            <FlavorList site={props.site} />
        </Form>
    );
}

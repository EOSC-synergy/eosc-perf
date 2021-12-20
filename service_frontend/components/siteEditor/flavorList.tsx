import { Flavor, Flavors, Site } from 'model';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { Card, Form } from 'react-bootstrap';
import { LoadingOverlay } from 'components/loadingOverlay';
import { FlavorEditor } from 'components/siteEditor/flavorEditor';
import React, { ReactElement } from 'react';
import { NewFlavor } from 'components/siteEditor/newFlavor';

export function FlavorList(props: { site: Site }): ReactElement {
    const flavors = useQuery(
        ['flavors', props.site.id],
        () => {
            return getHelper<Flavors>('/sites/' + props.site.id + '/flavors');
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
            refetchOnMount: 'always'
        }
    );

    return (
        <Form.Group className='mb-3'>
            <Form.Label>Flavors:</Form.Label>
            <Card style={{ maxHeight: '16rem' }} className='overflow-auto'>
                {flavors.isLoading && <LoadingOverlay />}
                {flavors.isSuccess &&
                    flavors.data &&
                    flavors.data.data.items.map((flavor: Flavor) => (
                        <FlavorEditor
                            flavor={flavor}
                            key={flavor.id}
                            refetch={flavors.refetch}
                        />
                    ))}
                <NewFlavor site={props.site} />
            </Card>
        </Form.Group>
    );
}

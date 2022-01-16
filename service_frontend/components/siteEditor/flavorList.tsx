import { Flavor, Flavors, Site } from 'model';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { Card, Col, Form, ListGroup, Row } from 'react-bootstrap';
import { LoadingOverlay } from 'components/loadingOverlay';
import { FlavorEditor } from 'components/siteEditor/flavorEditor';
import React, { ReactElement, useState } from 'react';
import { NewFlavor } from 'components/siteEditor/newFlavor';
import { Paginator } from '../pagination';

export function FlavorList(props: { site: Site }): ReactElement {
    const [page, setPage] = useState(1);

    const flavors = useQuery(
        ['flavors', props.site.id],
        () => {
            return getHelper<Flavors>('/sites/' + props.site.id + '/flavors', undefined, { page });
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
            refetchOnMount: 'always',
        }
    );

    return (
        <Form.Group className="mb-3">
            <Form.Label>Flavors:</Form.Label>
            <Card style={{ maxHeight: '16rem' }} className="overflow-auto">
                {flavors.isLoading && <LoadingOverlay />}
                {flavors.isSuccess &&
                    flavors.data &&
                    flavors.data.data.items.map((flavor: Flavor) => (
                        <FlavorEditor flavor={flavor} key={flavor.id} refetch={flavors.refetch} />
                    ))}

                <ListGroup.Item key="new-flavor">
                    <Row>
                        <Col>
                            <NewFlavor site={props.site} />{' '}
                        </Col>
                        {flavors.isSuccess && flavors.data && flavors.data.data.pages > 0 && (
                            <Col md="auto">
                                <Paginator
                                    pagination={flavors.data.data}
                                    navigateTo={(p) => setPage(p)}
                                />
                            </Col>
                        )}
                    </Row>
                </ListGroup.Item>
            </Card>
        </Form.Group>
    );
}

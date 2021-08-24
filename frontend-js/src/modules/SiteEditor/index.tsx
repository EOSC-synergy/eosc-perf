import React, { useState } from 'react';
import { Col, Container, ListGroup, Row } from 'react-bootstrap';
import { Site, Sites } from '../../api';
import { useQuery } from 'react-query';
import { getHelper } from '../../api-helpers';
import { LoadingOverlay } from '../loadingOverlay';
import { SiteEditor } from './siteEditor';

function SiteSelect(props: { site: Site; setActiveSite: (site: Site) => void }) {
    return (
        <ListGroup.Item onClick={(e) => props.setActiveSite(props.site)} action>
            <div className="d-flex w-100 justify-content-between">
                <h5 className="mb-1">{props.site.name}</h5>
                <small>{props.site.id}</small>
            </div>
            <p className="mb-1">{props.site.description}</p>
            <small>{props.site.address}</small>
        </ListGroup.Item>
    );
}

function SitesEditor(props: { token: string }) {
    let { status, isLoading, isError, data, isSuccess, refetch } = useQuery(
        'sites',
        () => {
            return getHelper<Sites>('/sites', props.token);
        },
        {
            enabled: !!props.token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    const [activeSite, setActiveSite] = useState<Site | null>(null);

    // TODO: pagination

    return (
        <Container>
            <Row>
                <Col>
                    <ListGroup>
                        {isLoading && <LoadingOverlay />}
                        {isSuccess && data && data.data.items!.length === 0 && 'No sites found!'}
                        {isSuccess &&
                            data &&
                            data.data.items!.map((site: Site) => (
                                <SiteSelect
                                    site={site}
                                    setActiveSite={setActiveSite}
                                    key={site.id}
                                />
                            ))}
                    </ListGroup>
                </Col>
                <Col>
                    {activeSite != null && (
                        <SiteEditor
                            token={props.token}
                            key={activeSite.id}
                            site={activeSite}
                            refetch={refetch}
                        />
                    )}
                </Col>
            </Row>
        </Container>
    );
}

const SiteEditorModule = {
    path: '/site-editor',
    element: SitesEditor,
    name: 'SiteEditor',
    dropdownName: 'Site editor',
};
export default SiteEditorModule;
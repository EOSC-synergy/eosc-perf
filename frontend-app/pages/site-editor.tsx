import React, { ReactElement, useState } from 'react';
import { Col, Container, ListGroup, Row } from 'react-bootstrap';
import { Site, Sites } from 'model';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { LoadingOverlay } from 'components/loadingOverlay';
import { SiteEditor } from 'components/siteEditor/siteEditor';

function SiteSelect(props: {
    site: Site;
    setActiveSite: (site: Site) => void;
}): ReactElement {
    return (
        <ListGroup.Item onClick={() => props.setActiveSite(props.site)} action>
            <div className='d-flex w-100 justify-content-between'>
                <h5 className='mb-1'>{props.site.name}</h5>
                <small>{props.site.id}</small>
            </div>
            <p className='mb-1'>{props.site.description}</p>
            <small>{props.site.address}</small>
        </ListGroup.Item>
    );
}

/**
 * Admin-only page to edit sites in the database and add flavors.
 *
 * @returns {React.ReactElement}
 * @constructor
 */
function SitesEditor(): ReactElement {
    const sites = useQuery(
        'sites',
        () => {
            return getHelper<Sites>('/sites');
        },
        {
            refetchOnWindowFocus: false // do not spam queries
        }
    );

    const [activeSite, setActiveSite] = useState<Site | null>(null);

    // TODO: pagination

    return (
        <Container>
            <Row>
                <Col>
                    <ListGroup>
                        {sites.isLoading && <LoadingOverlay />}
                        {sites.isSuccess &&
                            sites.data &&
                            sites.data.data.items.length === 0 &&
                            'No sites found!'}
                        {sites.isSuccess &&
                            sites.data &&
                            sites.data.data.items.map((site: Site) => (
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
                            key={activeSite.id}
                            site={activeSite}
                            refetch={sites.refetch}
                        />
                    )}
                </Col>
            </Row>
        </Container>
    );
}

export default SitesEditor;

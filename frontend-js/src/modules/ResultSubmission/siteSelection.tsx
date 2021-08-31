import { useQuery } from 'react-query';
import { getHelper } from '../../api-helpers';
import { Flavors, Sites } from '../../api';
import { Card, Form } from 'react-bootstrap';
import React from 'react';

export function SiteSelection(props: {
    siteId?: string;
    setSiteId: (siteId: string) => void;
    flavorId?: string;
    setFlavorId: (flavorId: string) => void;
}) {
    let sites = useQuery(
        'sites',
        () => {
            return getHelper<Sites>('/sites');
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    let flavors = useQuery(
        'flavors-' + props.siteId,
        () => {
            return getHelper<Flavors>('/sites/' + props.siteId + '/flavors');
        },
        {
            enabled: sites.isSuccess && props.siteId !== undefined,
            refetchOnWindowFocus: false,
        }
    );

    return (
        <>
            <Form.Group>
                <Form.Label>Select execution site:</Form.Label>
                <Form.Control
                    as="select"
                    onChange={(e) => props.setSiteId(e.target.value)}
                    value={props.siteId}
                >
                    {sites.isSuccess &&
                        sites.data.data.items!.map((site) => (
                            <option value={site.id} key={site.id}>
                                {site.name}
                            </option>
                        ))}
                </Form.Control>
            </Form.Group>
            {sites.isSuccess && props.siteId && (
                <Form.Group>
                    <Form.Label>Select machine flavor:</Form.Label>
                    <Form.Control
                        as="select"
                        onChange={(e) => props.setFlavorId(e.target.value)}
                        value={props.flavorId}
                    >
                        {flavors.isSuccess &&
                            flavors.data.data.items!.map((flavor) => (
                                <option value={flavor.name} key={flavor.id}>
                                    {flavor.name}
                                </option>
                            ))}
                    </Form.Control>
                </Form.Group>
            )}
            {/* TODO: add site button */}
            {/* <Form.Group>
                    <label htmlFor="siteFlavorCustom"></label>
                    <textarea
                        className="form-control d-none"
                        id="siteFlavorCustom"
                        name="siteFlavorCustom"
                        placeholder="Enter more details about your custom flavor here..."
                    ></textarea>
                </Form.Group>;
                <div id="customSiteInfo" className="d-none">
                    <div className="m-2">
                        <label htmlFor="site_name">Site name</label>
                        <br />
                        <input
                            type="text"
                            id="site_name"
                            className="form-control"
                            placeholder="KIT Cluster"
                            disabled
                        />
                    </div>
                    <div className="m-2">
                        <label htmlFor="site_address">Site address</label>
                        <br />
                        <input
                            type="text"
                            id="site_address"
                            className="form-control"
                            placeholder="cluster.kit.edu"
                            disabled
                        />
                    </div>
                    <div className="m-2">
                        <label htmlFor="site_description">Site description</label>
                        <br />
                        <input
                            type="text"
                            id="site_description"
                            className="form-control"
                            placeholder="Very good"
                            disabled
                        />
                    </div>
                    <div className="m-2">
                        <label htmlFor="customSiteFlavor">Machine flavor name:</label>
                        <br />
                        <input
                            type="text"
                            id="customSiteFlavor"
                            className="form-control"
                            placeholder="unknown"
                            disabled
                        />
                    </div>
                </div> */}{' '}
        </>
    );
}

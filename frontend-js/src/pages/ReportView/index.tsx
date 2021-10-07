import React, { ReactElement, useContext, useState } from 'react';
import { Alert, Col, Container, ListGroup, Row } from 'react-bootstrap';
import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';
import { Claim, Claims, Submit, Submits } from 'api';

import '../../actionable.css';
import { BenchmarkInfo } from 'pages/ReportView/benchmarkInfo';
import { SiteInfo } from 'pages/ReportView/siteInfo';
import { FlavorInfo } from 'pages/ReportView/flavorInfo';
import { UserContext } from 'userContext';
import { PageBase } from '../pageBase';
import { ClaimInteraction } from 'pages/ReportView/claimInteraction';
import { SubmitInteraction } from 'pages/ReportView/submitInteraction';
import { ClaimInfo } from 'pages/ReportView/claimInfo';

function SubmitView(props: { submit: Submit; refetch: () => void }) {
    const [opened, setOpened] = useState(false);

    // TODO: pagination

    return (
        <ListGroup.Item>
            <div
                className="actionable"
                onClick={() => {
                    setOpened(!opened);
                }}
            >
                <div className="w-100 d-flex justify-content-between">
                    <h5 className="mb-1">{props.submit.resource_type}</h5>
                    <small>{props.submit.upload_datetime}</small>
                </div>
                <p className="mb-1">{/*props.submit.message*/}</p>
                <small className="text-muted">For {props.submit.resource_id}</small>
            </div>
            {opened && (
                <>
                    <hr />
                    {props.submit.resource_type === 'site' && (
                        <SiteInfo id={props.submit.resource_id} />
                    )}
                    {props.submit.resource_type === 'flavor' && (
                        <FlavorInfo id={props.submit.resource_id} />
                    )}
                    {props.submit.resource_type === 'benchmark' && (
                        <BenchmarkInfo id={props.submit.resource_id} />
                    )}
                    {props.submit.resource_type === 'claim' && (
                        <ClaimInfo id={props.submit.resource_id} />
                    )}
                    <SubmitInteraction submit={props.submit} refetch={props.refetch} />
                </>
            )}
        </ListGroup.Item>
    );
}

function ClaimView(props: { claim: Claim; refetch: () => void }) {
    const [opened, setOpened] = useState(false);

    // TODO: pagination

    return (
        <ListGroup.Item>
            <div
                className="actionable"
                onClick={() => {
                    setOpened(!opened);
                }}
            >
                <div className="w-100 d-flex justify-content-between">
                    <h5 className="mb-1">{props.claim.resource_type}</h5>
                    <small>{props.claim.upload_datetime}</small>
                </div>
                <p className="mb-1">{props.claim.message}</p>
                <small className="text-muted">For {props.claim.resource_id}</small>
            </div>
            {opened && (
                <>
                    <hr />
                    {/* TODO: reuse claim data from props instead of id */}
                    <ClaimInfo id={props.claim.id} />
                    <ClaimInteraction claim={props.claim} refetch={props.refetch} />
                </>
            )}
        </ListGroup.Item>
    );
}

function ReportsView(): ReactElement {
    const auth = useContext(UserContext);

    const submits = useQuery(
        'submits',
        () => {
            return getHelper<Submits>('/reports/submits', auth.token, {});
        },
        {
            enabled: !!auth.token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );
    const claims = useQuery(
        'claims',
        () => {
            return getHelper<Claims>('/reports/claims', auth.token, {});
        },
        {
            enabled: !!auth.token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <Container>
            {auth.token === undefined && (
                <Alert variant="danger" className="mt-3">
                    You must be logged in to use this page!
                </Alert>
            )}
            <Row className="my-3">
                <Col>
                    <h1>Submits</h1>
                    <ListGroup>
                        {submits.isSuccess &&
                            submits.data &&
                            submits.data.data.items.map((submit) => (
                                <SubmitView
                                    submit={submit}
                                    key={submit.resource_id}
                                    refetch={submits.refetch}
                                />
                            ))}
                        {submits.isSuccess && submits.data.data.total === 0 && (
                            <>No submits to display!</>
                        )}
                        {submits.isError && <>Failed to fetch submits!</>}
                    </ListGroup>
                </Col>
                <Col>
                    <h1>Claims</h1>
                    <ListGroup>
                        {claims.isSuccess &&
                            claims.data &&
                            claims.data.data.items.map((claim) => (
                                <ClaimView
                                    claim={claim}
                                    key={claim.resource_id}
                                    refetch={claims.refetch}
                                />
                            ))}
                        {claims.isSuccess && claims.data.data.total === 0 && (
                            <>No claims to display!</>
                        )}
                        {claims.isError && <>Failed to fetch claims!</>}
                    </ListGroup>
                </Col>
            </Row>
        </Container>
    );
}

const ReportViewModule: PageBase = {
    path: '/view-reports',
    element: ReportsView,
    name: 'ReportsView',
    displayName: 'View reports',
};
export default ReportViewModule;

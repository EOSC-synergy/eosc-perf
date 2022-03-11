import React, { ReactElement, useContext, useEffect, useState } from 'react';
import { Col, Container, ListGroup, Row } from 'react-bootstrap';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { Claim, Claims, Submit, Submits } from 'model';

import actionable from 'styles/actionable.module.css';
import { BenchmarkInfo } from 'components/reportView/benchmarkInfo';
import { SiteInfo } from 'components/reportView/siteInfo';
import { FlavorInfo } from 'components/reportView/flavorInfo';
import { UserContext } from 'components/userContext';
import { ClaimInteraction } from 'components/reportView/claimInteraction';
import { SubmitInteraction } from 'components/reportView/submitInteraction';
import { ClaimInfo } from 'components/reportView/claimInfo';
import { Paginator } from '../components/pagination';
import Head from 'next/head';
import { useRouter } from 'next/router';

function SubmitView(props: { submit: Submit; refetch: () => void }) {
    const [opened, setOpened] = useState(false);

    return (
        <ListGroup.Item>
            <div
                className={actionable.actionable}
                onClick={() => {
                    setOpened(!opened);
                }}
            >
                <div className="w-100 d-flex justify-content-between">
                    <h5 className="mb-1">{props.submit.resource_type}</h5>
                    <small>{props.submit.upload_datetime}</small>
                </div>
                <small className="text-muted">Submitted by {props.submit.uploader.email}</small>
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
                    {/*props.submit.resource_type === 'claim' && (
                        <ClaimInfo id={props.submit.resource_id} />
                    )*/}
                    <SubmitInteraction submit={props.submit} refetch={props.refetch} />
                </>
            )}
        </ListGroup.Item>
    );
}

function ClaimView(props: { claim: Claim; refetch: () => void }) {
    const [opened, setOpened] = useState(false);

    return (
        <ListGroup.Item>
            <div
                className={actionable.actionable}
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
                    <ClaimInfo claim={props.claim} />
                    <ClaimInteraction claim={props.claim} refetch={props.refetch} />
                </>
            )}
        </ListGroup.Item>
    );
}

/**
 * Admin-only page to view pending reports and submissions.
 *
 * @returns {React.ReactElement}
 * @constructor
 */
function ReportsView(): ReactElement {
    const auth = useContext(UserContext);
    const router = useRouter();

    const [submitsPage, setSubmitsPage] = useState(1);
    const [claimsPage, setClaimsPage] = useState(1);

    // if user is not admin, redirect them away
    useEffect(() => {
        if (!auth.loading && !auth.admin) {
            router.push('/');
        }
    }, [router, auth.admin, auth.loading]);

    const submits = useQuery(
        ['submits', submitsPage],
        () => {
            return getHelper<Submits>('/reports/submits', auth.token, { page: submitsPage });
        },
        {
            enabled: !!auth.token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );
    const claims = useQuery(
        ['claims', claimsPage],
        () => {
            return getHelper<Claims>('/reports/claims', auth.token, { page: claimsPage });
        },
        {
            enabled: !!auth.token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    function SubmitsList() {
        return (
            <>
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
                {submits.isSuccess && submits.data && submits.data.data.pages > 0 && (
                    <div className="mt-2">
                        <Paginator
                            pagination={submits.data.data}
                            navigateTo={(p) => setSubmitsPage(p)}
                        />
                    </div>
                )}
            </>
        );
    }

    function ClaimsList() {
        return (
            <>
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
                    {claims.isSuccess && claims.data.data.total === 0 && <>No claims to display!</>}
                    {claims.isError && <>Failed to fetch claims!</>}
                </ListGroup>
                {claims.isSuccess && claims.data && claims.data.data.pages > 0 && (
                    <div className="mt-2">
                        <Paginator
                            pagination={claims.data.data}
                            navigateTo={(p) => setClaimsPage(p)}
                        />
                    </div>
                )}
            </>
        );
    }

    return (
        <>
            <Head>
                <title>Reports View</title>
            </Head>
            <Container>
                {auth.admin && (
                    <>
                        <Row className="my-3">
                            <Col>
                                <h1>Submits</h1>
                                <SubmitsList />
                            </Col>
                            <Col>
                                <h1>Claims</h1>
                                <ClaimsList />
                            </Col>
                        </Row>
                    </>
                )}
            </Container>
        </>
    );
}

export default ReportsView;

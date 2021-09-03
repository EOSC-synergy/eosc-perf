import React, { useContext, useState } from 'react';
import { Badge, Container, ListGroup } from 'react-bootstrap';
import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';
import { Report, Reports } from 'api';

import '../../actionable.css';
import { BenchmarkReportInfo } from './benchmarkReportInfo';
import { ResultReportInfo } from './resultReportInfo';
import { SiteReportInfo } from './siteReportInfo';
import { FlavorReportInfo } from './flavorReportInfo';
import { UserContext } from 'userContext';
import { PageBase } from '../pageBase';

function ReportView(props: { report: Report; refetch: () => void }) {
    let [opened, setOpened] = useState(false);

    // TODO: pagination

    return (
        <ListGroup.Item>
            <div
                className="actionable"
                onClick={() => {
                    setOpened(!opened);
                }}
            >
                {/*item.classList.add("list-group-item", "list-group-item-action", "flex-column",
                        "align-items-start");*/}
                <div className="w-100">
                    {/* headingDiv.classList.add("d-flex","w-100", "justify-content-between"); */}
                    <h5 className="mb-1">{props.report.resource_type}</h5>
                    <small>{props.report.id}</small>
                </div>
                <p className="mb-1">{props.report.message}</p>
                <div>
                    {/*footerDiv.classList.add("d-flex", "w-100", "justify-content-between"); */}
                    {/* TODO: uploader! */}
                    {/*<small>{report.uploader}</small>*/}
                    <small>
                        <Badge
                            bg={
                                props.report.verdict
                                    ? 'success'
                                    : props.report.verdict === null
                                    ? 'secondary'
                                    : 'danger'
                            }
                        >
                            {props.report.verdict
                                ? 'Approved'
                                : props.report.verdict === null
                                ? 'Pending'
                                : 'Rejected'}
                        </Badge>
                    </small>
                </div>
            </div>
            {opened && (
                <>
                    <hr />
                    {props.report.resource_type == 'site' && <SiteReportInfo {...props} />}
                    {props.report.resource_type == 'flavor' && <FlavorReportInfo {...props} />}
                    {props.report.resource_type == 'benchmark' && (
                        <BenchmarkReportInfo {...props} />
                    )}
                    {props.report.resource_type == 'result' && <ResultReportInfo {...props} />}
                </>
            )}
        </ListGroup.Item>
    );
}

function ReportsView() {
    const auth = useContext(UserContext);

    let { data, isSuccess, refetch } = useQuery(
        'reports',
        () => {
            return getHelper<Reports>('/reports', auth.token, {});
        },
        {
            enabled: !!auth.token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <Container>
            <h1>Reports</h1>
            <ListGroup>
                {isSuccess &&
                    data &&
                    data.data.items!.map((report) => (
                        <ReportView report={report} key={report.id} refetch={refetch} />
                    ))}
            </ListGroup>
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
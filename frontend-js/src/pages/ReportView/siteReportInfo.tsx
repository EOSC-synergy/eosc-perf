import { Report, Site } from '../../api';
import { useQuery } from 'react-query';
import { getHelper } from '../../api-helpers';
import { LoadingOverlay } from '../../components/loadingOverlay';
import { ReportInteraction } from './reportInteraction';
import React from 'react';

export function SiteReportInfo(props: { report: Report; refetch: () => void }) {
    let { isLoading, data, isSuccess } = useQuery(
        'site-' + props.report.resource_id,
        () => {
            return getHelper<Site>('/sites/' + props.report.resource_id);
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <>
            {isLoading && <LoadingOverlay />}
            {isSuccess && data && (
                <>
                    New site: {data.data.name}
                    <br />
                    Address: {data.data.address}
                    <br />
                    Description: {data.data.description}
                    <br />
                    {/* Uploader: {{ uploader_name }} ({{ uploader_mail }})<br/> */}
                    Upload date: {props.report.upload_date}
                    <br />
                    <ReportInteraction {...props} />
                </>
            )}
        </>
    );
}

import { Report, Site } from '../../api';
import { useQuery } from 'react-query';
import { getHelper } from '../../api-helpers';
import { LoadingOverlay } from '../loadingOverlay';
import { ReportInteraction } from './reportInteraction';
import React from 'react';

export function SiteReportInfo(props: { report: Report; token: string; refetch: () => void }) {
    let { isLoading, data, isSuccess } = useQuery(
        'site',
        () => {
            return getHelper<Site>('/sites/' + props.report.resource_id);
        },
        {
            enabled: !!props.token,
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
                    Description: {data.data.description}
                    <br />
                    {/* Uploader: {{ uploader_name }} ({{ uploader_mail }})<br/> */}
                    Upload date: {props.report.created_at}
                    <br />
                    <ReportInteraction {...props} />
                </>
            )}
        </>
    );
}

import { Benchmark, Flavor, Report } from '../../api';
import React from 'react';
import { useQuery } from 'react-query';
import { getHelper } from '../../api-helpers';
import { LoadingOverlay } from '../loadingOverlay';
import { ReportInteraction } from './reportInteraction';

export function FlavorReportInfo(props: { report: Report; token: string; refetch: () => void }) {
    let { isLoading, data, isSuccess } = useQuery(
        'flavor',
        () => {
            return getHelper<Flavor>('/sites/flavors/' + props.report.resource_id);
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
                    New flavor: {data.data.name}
                    <br />
                    {/* TODO: site info? how? */}
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

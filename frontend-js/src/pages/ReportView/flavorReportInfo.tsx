import { Flavor, Report } from '../../api';
import React from 'react';
import { useQuery } from 'react-query';
import { getHelper } from '../../api-helpers';
import { LoadingOverlay } from '../loadingOverlay';
import { ReportInteraction } from './reportInteraction';

export function FlavorReportInfo(props: { report: Report; refetch: () => void }) {
    let { isLoading, data, isSuccess } = useQuery(
        'flavor-' + props.report.resource_id,
        () => {
            return getHelper<Flavor>('/sites/flavors/' + props.report.resource_id);
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
                    New flavor: {data.data.name}
                    <br />
                    {/* TODO: site info? how? */}
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

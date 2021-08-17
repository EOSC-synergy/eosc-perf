import { Benchmark, Report } from '../../api';
import { useQuery } from 'react-query';
import { getHelper } from '../../api-helpers';
import { LoadingOverlay } from '../loadingOverlay';
import { ReportInteraction } from './reportInteraction';
import React from 'react';

export function BenchmarkReportInfo(props: { report: Report; token: string; refetch: () => void }) {
    let { isLoading, data, isSuccess } = useQuery(
        'benchmark',
        () => {
            return getHelper<Benchmark>('/benchmarks/' + props.report.resource_id);
        },
        {
            enabled: !!props.token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    const dockerHubLink = 'https://hub.docker.com/repository/docker/' + data?.data.docker_image;

    return (
        <>
            {isLoading && <LoadingOverlay />}
            {isSuccess && data && (
                <>
                    <p>
                        {/* TODO: uploader */}
                        {/*Uploader: {{ uploader_name }} ({{ uploader_mail }})<br /> */}
                        Description: {data.data.description}
                        <br />
                        Date: {props.report.created_at}
                    </p>
                    <a href={dockerHubLink}>{data.data.docker_image}</a>
                    <br />
                    {/* TODO: markdown parser */}
                    {/*<div id="docker_desc" className="jumbotron" style="overflow:scroll;height:60%">
                          {{ docker_desc | safe}}
                      </div> */}
                    <ReportInteraction {...props} />
                </>
            )}
        </>
    );
}

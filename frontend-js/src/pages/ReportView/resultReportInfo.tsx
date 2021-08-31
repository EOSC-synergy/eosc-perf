import { Report, Result } from '../../api';
import { useQuery } from 'react-query';
import { getHelper } from '../../api-helpers';
import { LoadingOverlay } from '../../components/loadingOverlay';
import React from 'react';

export function ResultReportInfo(props: { report: Report; refetch: () => void }) {
    let { isLoading, data, isSuccess } = useQuery(
        'result-' + props.report.resource_id,
        () => {
            return getHelper<Result>('/results/' + props.report.resource_id);
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <>
            {isLoading && <LoadingOverlay />}
            {isSuccess && data && (
                <p>
                    {/* TODO: *reporter* info */}
                    {/* Reported by: {{ reporter_name }} ({{ reporter_mail }})<br /> */}
                    Message: {props.report.message}
                    <br />
                    Date: {props.report.upload_date}
                    <br />
                    Site: {data.data.site.name}
                    <br />
                    Benchmark: {data.data.benchmark.docker_image + data.data.benchmark.docker_tag}
                    <br />
                    {/* Uploader: {{ uploader_name }} ({{ uploader_mail }})<br /> */}
                    Tags: {data.data.tags.map((tag) => tag.name).join(', ')}
                    <br />
                    JSON:
                    <pre>
                        <code
                            className="json rounded"
                            style={{ overflow: 'scroll', maxHeight: '60vh' }}
                        >
                            {JSON.stringify(data.data.json, null, 4)}
                        </code>
                    </pre>
                </p>
            )}
        </>
    );
}

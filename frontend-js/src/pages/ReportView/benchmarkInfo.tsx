import React, { ReactElement } from 'react';
import { Benchmark } from 'api';
import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';
import { LoadingOverlay } from 'components/loadingOverlay';

export function BenchmarkInfo(props: { id: string }): ReactElement {
    const { isLoading, data, isSuccess } = useQuery(
        'benchmark-' + props.id,
        () => {
            return getHelper<Benchmark>('/benchmarks/' + props.id);
        },
        {
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
                    </p>
                    <a href={dockerHubLink}>{data.data.docker_image}</a>
                    <br />
                    {/* TODO: markdown parser */}
                    {/*<div id="docker_desc" className="jumbotron" style="overflow:scroll;height:60%">
                          {{ docker_desc | safe}}
                      </div> */}
                </>
            )}
        </>
    );
}

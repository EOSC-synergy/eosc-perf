import React, { ReactElement } from 'react';
import { Benchmark } from 'api';
import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';
import { LoadingOverlay } from 'components/loadingOverlay';
import { benchmarkLinkDisplay, truthyOrNoneTag } from 'utility';

export function BenchmarkInfo(props: { id: string }): ReactElement {
    const { isLoading, data, isSuccess } = useQuery(
        ['benchmark', props.id],
        () => {
            return getHelper<Benchmark>('/benchmarks/' + props.id);
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
                    {/* TODO: uploader */}
                    {/*Uploader: {{ uploader_name }} ({{ uploader_mail }})<br /> */}
                    Image: {benchmarkLinkDisplay(data.data)}
                    <br />
                    Description: {truthyOrNoneTag(data.data.description)}
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

import React, { ReactElement } from 'react';
import { Benchmark } from 'model';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { LoadingOverlay } from 'components/loadingOverlay';
import { benchmarkLinkDisplay, truthyOrNoneTag } from 'components/utility';

export function BenchmarkInfo(props: { id: string }): ReactElement {
    const benchmark = useQuery(
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
            {benchmark.isLoading && <LoadingOverlay />}
            {benchmark.isSuccess && benchmark.data && (
                <>
                    Image: {benchmarkLinkDisplay(benchmark.data.data)}
                    <br />
                    Description: {truthyOrNoneTag(benchmark.data.data.description)}
                    <br />
                    Submitted on: {new Date(benchmark.data.data.upload_datetime).toLocaleString()}
                </>
            )}
        </>
    );
}

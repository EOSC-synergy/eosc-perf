import { Benchmark } from 'model';
import React, { ReactElement, useState } from 'react';
import { BenchmarkSubmissionModal } from 'components/submissionModals/benchmarkSubmissionModal';
import { SearchingSelector } from 'components/searchSelectors/index';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';

export function BenchmarkSearchSelect(props: {
    benchmark?: Benchmark;
    initBenchmark?: (benchmark?: Benchmark) => void;
    setBenchmark: (benchmark?: Benchmark) => void;
    initialBenchmarkId?: string;
}): ReactElement {
    useQuery(
        ['initial-benchmark', props.initialBenchmarkId],
        () => {
            return getHelper<Benchmark>('/benchmarks/' + props.initialBenchmarkId);
        },
        {
            enabled: props.initialBenchmarkId !== undefined,
            refetchOnWindowFocus: false, // do not spam queries
            onSuccess: (data) => {
                if (props.initBenchmark) {
                    props.initBenchmark(data.data);
                } else {
                    props.setBenchmark(data.data);
                }
            },
        }
    );

    function display(benchmark?: Benchmark) {
        return (
            <>
                Benchmark:{' '}
                {benchmark ? (
                    <a href={'https://hub.docker.com/r/' + benchmark.docker_image}>
                        {benchmark.docker_image + ':' + benchmark.docker_tag}
                    </a>
                ) : (
                    <div className="text-muted" style={{ display: 'inline-block' }}>
                        None
                    </div>
                )}
            </>
        );
    }

    function displayRow(benchmark: Benchmark) {
        return (
            <>
                {benchmark.docker_image + ':' + benchmark.docker_tag}
                <div>
                    {benchmark.description}
                    <br />
                </div>
            </>
        );
    }

    const [showSubmitModal, setShowSubmitModal] = useState(false);

    return (
        <>
            <SearchingSelector<Benchmark>
                queryKeyPrefix="benchmark"
                tableName="Benchmark"
                endpoint="/benchmarks:search"
                item={props.benchmark}
                setItem={props.setBenchmark}
                display={display}
                displayRow={displayRow}
                submitNew={() => setShowSubmitModal(true)}
            />
            <BenchmarkSubmissionModal
                show={showSubmitModal}
                onHide={() => setShowSubmitModal(false)}
            />
        </>
    );
}

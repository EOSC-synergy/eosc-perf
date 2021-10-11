import { Benchmark } from 'api';
import React, { ReactElement, useState } from 'react';
import { BenchmarkSubmissionModal } from 'components/submissionModals/benchmarkSubmissionModal';
import { SimpleSearchPopover } from 'components/searchPopover/index';

export function BenchmarkSearchPopover(props: {
    benchmark?: Benchmark;
    setBenchmark: (benchmark?: Benchmark) => void;
}): ReactElement {
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
                <a
                    href="#"
                    title={benchmark.docker_image + ':' + benchmark.docker_tag}
                    onClick={() => props.setBenchmark(benchmark)}
                >
                    {benchmark.docker_image + ':' + benchmark.docker_tag}
                </a>
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
            <SimpleSearchPopover<Benchmark>
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

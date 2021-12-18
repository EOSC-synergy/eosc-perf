import React, { ReactElement } from 'react';
import { Result } from 'model';
import { Ordered } from 'components/ordered';

export function BenchmarkColumn(props: {
    result: Ordered<Result>;
}): ReactElement {
    return (
        <>
            {props.result.benchmark.docker_image +
                ':' +
                props.result.benchmark.docker_tag}
        </>
    );
}

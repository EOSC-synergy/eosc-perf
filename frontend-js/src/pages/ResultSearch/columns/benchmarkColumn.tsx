import React, { ReactElement } from 'react';
import { Result } from 'api';

export function BenchmarkColumn(props: { result: Result }): ReactElement {
    return <>{props.result.benchmark.docker_image + ':' + props.result.benchmark.docker_tag}</>;
}

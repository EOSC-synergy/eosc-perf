import { Result } from 'api';

export function BenchmarkColumn(props: { result: Result }) {
    return <>{props.result.benchmark.docker_image + ':' + props.result.benchmark.docker_tag}</>;
}

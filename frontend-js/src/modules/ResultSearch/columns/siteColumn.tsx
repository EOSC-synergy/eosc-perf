import { Result } from '../../../api';

export function SiteColumn(props: { result: Result }) {
    return <>{props.result.site.name}</>;
}

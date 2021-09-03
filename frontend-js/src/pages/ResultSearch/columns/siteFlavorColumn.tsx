import { Result } from 'api';

export function SiteFlavorColumn(props: { result: Result }) {
    return <>{props.result.flavor.name}</>;
}

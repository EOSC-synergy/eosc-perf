import { Result } from 'api';
import { fetchSubkey } from '../jsonKeyHelpers';

export function CustomColumn(props: { result: Result; jsonKey: string }) {
    const value = fetchSubkey(props.result.json, props.jsonKey);
    return <>{value ? value.toString() : <div className="text-muted">Not found!</div>}</>;
}

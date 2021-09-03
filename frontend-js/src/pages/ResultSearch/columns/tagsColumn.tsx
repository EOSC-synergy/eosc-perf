import { Result } from 'api';

export function TagsColumn(props: { result: Result }) {
    return (
        <>
            {props.result.tags.length ? (
                props.result.tags.join(', ')
            ) : (
                <div className="text-muted">None</div>
            )}
        </>
    );
}

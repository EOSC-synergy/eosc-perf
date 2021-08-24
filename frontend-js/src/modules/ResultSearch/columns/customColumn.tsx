import { Result } from '../../../api';

/**
 * Fetch a sub-key from an object, as noted by the filter JSON syntax.
 * @param obj The object to get the value from.
 * @param keyPath The path to the value.
 * @returns {*} Anything, or SUBKEY_NOT_FOUND_HINT if not found.
 * @private
 */
function fetchSubkey(obj: any, keyPath: string) {
    const keys = keyPath.split('.');
    let sub_item = obj;
    for (let sub_key of keys) {
        if (typeof sub_item === 'undefined') {
            return undefined;
        }
        sub_item = sub_item[sub_key];
    }
    return sub_item;
}

export function CustomColumn(props: { result: Result; jsonKey: string }) {
    const value = fetchSubkey(props.result.json, props.jsonKey);
    return <>{value ? value.toString() : 'Not found!'}</>;
}

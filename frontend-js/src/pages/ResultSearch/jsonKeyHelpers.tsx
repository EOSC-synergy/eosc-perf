export type Json = string | number | boolean | null | Json[] | { [key: string]: Json };

/**
 * Fetch a sub-key from an object, as noted by the filter JSON syntax.
 * @param {Json} obj The object to navigate.
 * @param {string} keyPath The path to the value to read.
 * @returns unknown The desired value, or undefined
 */
export function fetchSubkey(obj: Json, keyPath: string): unknown {
    const keys = keyPath.split('.');
    let sub_item: Json = obj;
    for (const sub_key of keys) {
        if (sub_item === 'undefined' || sub_item === null) {
            return undefined;
        }
        if (typeof sub_item !== 'object') {
            return undefined;
        }
        sub_item = (sub_item as Record<string, Json>)[sub_key];
    }
    return sub_item;
}

/**
 * Get the name of the specific/final key accessed by a key-path of the filter JSON syntax.
 * @param keyPath The path to the value.
 * @returns {*|string} The name of the specified key.
 */
export function getSubkeyName(keyPath: string): string {
    const keys = keyPath.split('.');
    return keys[keys.length - 1];
}

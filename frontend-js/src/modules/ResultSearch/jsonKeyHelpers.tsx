/**
 * Fetch a sub-key from an object, as noted by the filter JSON syntax.
 * @param obj The object to get the value from.
 * @param keyPath The path to the value.
 * @returns {*} Anything, or SUBKEY_NOT_FOUND_HINT if not found.
 * @private
 */
export function fetchSubkey(obj: any, keyPath: string) {
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

/**
 * Get the name of the specific/final key accessed by a key-path of the filter JSON syntax.
 * @param keyPath The path to the value.
 * @returns {*|string} The name of the specified key.
 * @private
 */
export function getSubkeyName(keyPath: string) {
    let keys = keyPath.split('.');
    return keys[keys.length - 1];
}

import { Table } from './resultTable.mjs';

export const SUBKEY_NOT_FOUND_HINT = '⚠ not found';

/**
 * Fetch a sub-key from an object, as noted by the filter JSON syntax.
 * @param obj The object to get the value from.
 * @param key_path The path to the value.
 * @returns {*} Anything, or SUBKEY_NOT_FOUND_HINT if not found.
 * @private
 */
export function fetch_subkey(obj, key_path) {
    let keys = key_path.split('.');
    let sub_item = obj;
    for (let sub_key of keys) {
        if (typeof sub_item === 'undefined') {
            console.error('Failed to fetch subkey', key_path, 'from', obj);
            return SUBKEY_NOT_FOUND_HINT;
        }
        sub_item = sub_item[sub_key];
    }
    return sub_item;
}

/**
 * Get the name of the specific/final key accessed by a key-path of the filter JSON syntax.
 * @param key_path The path to the value.
 * @returns {*|string} The name of the specified key.
 * @private
 */
export function get_subkey_name(key_path) {
    let keys = key_path.split('.');
    return keys[keys.length - 1];
}

/**
 * Clear all entries of a select dropdown.
 * @param selectElement The dropdown to remove options from.
 * @private
 */
export function clear_select(selectElement) {
    while (selectElement.firstChild) {
        selectElement.removeChild(selectElement.firstChild);
    }
}

/**
 * Check if a keypath has valid syntax
 * @param key_path
 * @returns {boolean}
 * @private
 */
export function validate_keypath(key_path) {
    // alpha_num(.alpha_num)*
    return /^[\d\w_]+(\.[\d\w_]+)*$/.test(key_path);
}

export const FIELDS = Object.freeze({
    BENCHMARK: 'Benchmark',
    SITE: 'Site',
    FLAVOR: 'Site flavour',
    TAGS: 'Tags',
    UPLOADER: 'Uploader',
});
export const JSON_KEYS = new Map([
    [FIELDS.BENCHMARK, 'benchmark'],
    [FIELDS.SITE, 'site'],
    [FIELDS.FLAVOR, 'flavor'],
    [FIELDS.TAGS, 'tags'],
    [FIELDS.CHECKBOX, 'selected'],
    [FIELDS.UPLOADER, 'uploader'],
]);

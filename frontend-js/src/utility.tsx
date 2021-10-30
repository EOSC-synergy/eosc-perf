import React from 'react';

/**
 * If a specified string is falsy, replace it with a muted gray "None" text or similar
 * @param {string | undefined | null} value input String to evaluate
 * @param {string} altText Text to display instead of "None"
 * @returns {JSX.Element | string} Either a div with gray None text or the original string.
 */
export function truthyOrNoneTag(value: string | undefined | null, altText = 'None') {
    if (!value) {
        return (
            <div className="text-muted" style={{ display: 'inline' }}>
                {altText}
            </div>
        );
    }
    return value;
}

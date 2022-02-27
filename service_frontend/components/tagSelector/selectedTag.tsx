import { Tag } from '../../model';
import style from 'styles/tagSelector.module.css';
import { InlineCloseButton } from '../inlineCloseButton';
import React from 'react';

/**
 * Represents a selected tag
 * @param {Tag} props.tag selected tag
 * @param {(tag: Tag) => void} props.unselect callback to un-select tag
 * @constructor
 */
export function SelectedTag(props: { tag: Tag; unselect: (tag: Tag) => void }) {
    return (
        <div className={style.tagBadge + ' p-1'}>
            {props.tag.name}
            <InlineCloseButton onClose={() => props.unselect(props.tag)} />
        </div>
    );
}

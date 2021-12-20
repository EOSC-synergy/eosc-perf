import {Tag, Tags} from "../model";

export const tag: Tag = { id: 'test', name: 'testTag', description: null };
export const tags: Tags = {
    has_next: true,
    has_prev: false,
    next_num: 2,
    items: [tag],
    page: 1,
    pages: 2,
    per_page: 1,
    prev_num: 1,
    total: 2
};
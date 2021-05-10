import { search_page } from './searchPage.mjs';
import {
    fetch_subkey,
    FIELDS,
    get_subkey_name,
    JSON_KEYS,
    SUBKEY_NOT_FOUND_HINT,
} from './helpers.mjs';

/**
 * Prepare displayed data to be displayed prettily.
 *
 * This rounds floats et al to three decimals!
 *
 * @param item The items to display.
 * @returns {string} A nice-looking string.
 * @private
 */
function _format_column_data(item) {
    if (typeof item === 'undefined') {
        return SUBKEY_NOT_FOUND_HINT;
    }
    if (typeof item === 'number') {
        return (Math.round(item * 1000) / 1000).toString();
    }
    return item.toString();
}

/**
 * Generic comparison function helper
 * @param x first param
 * @param y second param
 * @returns {number} see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
 * @private
 */
function _comparator(x, y) {
    if (x < y) {
        return -1;
    }
    if (x > y) {
        return 1;
    }

    return 0;
}

export class Table {
    /**
     * Construct a new table handler.
     */
    constructor() {
        this.table = document.getElementById('result_table');
        this.columnHeads = new Map();
        this.resultElements = new Map();
        this.sortedBy = null;
    }

    /**
     * Label a result on the table as removed.
     *
     * This visually communicates the removal to the user.
     *
     * @param uuid uuid of result in displayed results
     */
    mark_result_as_removed(uuid) {
        let row = this.resultElements.get(uuid);
        if (row === undefined) {
            return;
        }

        const childCount = row.children.length;
        // clear columns
        clear_element_children(row);
        // darken the row
        let shadow = document.createElement('td');
        shadow.classList.add('loading-background');
        shadow.style.opacity = '100%';
        // add badge noting the removal of this result
        // TODO: this is a little ugly, restyle this
        let removedBadge = document.createElement('span');
        removedBadge.classList.add('badge', 'bg-danger');
        removedBadge.textContent = 'Removed';
        shadow.appendChild(removedBadge);
        shadow.colSpan = childCount;
        row.appendChild(shadow);
    }

    /**
     * Remove all entries from the table.
     */
    _clear() {
        while (this.table.firstChild != null) {
            this.table.firstChild.remove();
        }
        this.columnHeads.clear();
        this.resultElements.clear();
    }

    /**
     * Set up the top row of the table.
     */
    _create_head(columns) {
        let head = document.createElement('thead');
        for (const column of columns) {
            const column_name =
                column in Table.DEFAULT_COLUMNS
                    ? Table.DEFAULT_COLUMNS[column]
                    : get_subkey_name(column);

            let cell = document.createElement('th');
            this.columnHeads.set(column_name, {
                element: cell,
            });

            // if this is a custom/json-field column
            if (!(column in Table.DEFAULT_COLUMNS)) {
                cell.dataset.toggle = 'tooltip';
                cell.dataset.placement = 'top';
                cell.title = column;
                if (column.includes('.')) {
                    cell.textContent = '(...)' + column_name;
                } else {
                    cell.textContent = column_name;
                }
            } else {
                // hide label for checkbox column because wide and redundant
                // TODO: compare against the enum directly somehow instead of magic "CHECKBOX" string
                if (column === 'CHECKBOX') {
                    cell.textContent = '';
                } else {
                    cell.textContent = column_name;
                }
            }
            cell.scope = 'col';

            // add sorting callbacks
            const columnSortHelper = function (key) {
                return (x, y) => _comparator(x[key], y[key]);
            };

            switch (column_name) {
                case Table.DEFAULT_COLUMNS.CHECKBOX:
                case Table.DEFAULT_COLUMNS.BENCHMARK:
                case Table.DEFAULT_COLUMNS.SITE:
                case Table.DEFAULT_COLUMNS.FLAVOR:
                    {
                        // sort by selected results
                        cell.addEventListener('click', function () {
                            search_page.sort_by(
                                columnSortHelper(Table.COLUMN_KEYS.get(column_name)),
                                column_name
                            );
                        });
                    }
                    break;
                case Table.DEFAULT_COLUMNS.TAGS:
                    // TODO: is there a sensible order for a list of tags?
                    break;
                default:
                    cell.addEventListener('click', function () {
                        // TODO: sorting helpers
                        search_page.sort_by(
                            (x, y) =>
                                _comparator(
                                    fetch_subkey(x['data'], column),
                                    fetch_subkey(y['data'], column)
                                ),
                            column_name
                        );
                    });
                    break;
            }

            // if the column is being sorted by, add arrow/chevron
            if (this.sortedBy === column_name) {
                let arrow = document.createElement('i');
                arrow.classList.add('bi');
                if (this.sortReversed) {
                    arrow.classList.add('bi-chevron-up');
                } else {
                    arrow.classList.add('bi-chevron-down');
                }
                cell.appendChild(arrow);
            }
            head.appendChild(cell);
        }

        this.table.appendChild(head);
    }

    /**
     * Fill in results into the table.
     * @param results The results to fill the table with.
     * @param columns The columns to display.
     * @param startIndex The index of the first displayed item.
     */
    _fill_table(results, columns, startIndex) {
        for (let i = 0; i < results.length; i++) {
            let row = document.createElement('TR');
            const result = results[i];
            this.resultElements.set(result.uuid, row);

            // switch-case through columns as they may be in custom order
            for (const key of columns) {
                const column = key in Table.DEFAULT_COLUMNS ? Table.DEFAULT_COLUMNS[key] : key;
                let cell = document.createElement('TD');
                switch (column) {
                    case Table.DEFAULT_COLUMNS.CHECKBOX:
                        {
                            let select = document.createElement('input');
                            select.type = 'checkbox';
                            if (result[JSON_KEYS.get(FIELDS.CHECKBOX)]) {
                                select.checked = true;
                            }
                            // when clicked, select
                            select.addEventListener('click', function () {
                                search_page.select_result(i + startIndex);
                            });
                            cell.appendChild(select);
                        }
                        break;

                    case Table.DEFAULT_COLUMNS.FLAVOR:
                    case Table.DEFAULT_COLUMNS.SITE:
                    case Table.DEFAULT_COLUMNS.BENCHMARK:
                        {
                            cell.textContent = result[JSON_KEYS.get(column)];
                        }
                        break;

                    // handle tags specially because they could be empty
                    case Table.DEFAULT_COLUMNS.TAGS:
                        {
                            const content = result[JSON_KEYS.get(column)];
                            if (content.length === 0) {
                                cell.textContent = 'None';
                                cell.classList.add('text-muted');
                            } else {
                                cell.textContent = content;
                            }
                        }
                        break;

                    case Table.DEFAULT_COLUMNS.ACTIONS:
                        {
                            let div = document.createElement('div');
                            div.classList.add('btn-group');

                            // button to view json
                            let view_button = document.createElement('button');
                            view_button.type = 'button';
                            view_button.classList.add('btn', 'btn-primary', 'btn-sm');
                            view_button.addEventListener('click', function () {
                                search_page.display_result(result);
                            });
                            view_button.title = 'View JSON';
                            let viewButtonIcon = document.createElement('i');
                            viewButtonIcon.classList.add('bi', 'bi-hash');
                            view_button.appendChild(viewButtonIcon);
                            div.appendChild(view_button);

                            let actions_report = document.createElement('button');
                            actions_report.type = 'button';
                            actions_report.classList.add('btn', 'btn-warning', 'btn-sm');
                            actions_report.addEventListener('click', function () {
                                search_page.report_result(result);
                            });
                            actions_report.title = 'Report';
                            let reportButtonIcon = document.createElement('i');
                            reportButtonIcon.classList.add('bi', 'bi-exclamation');
                            actions_report.appendChild(reportButtonIcon);
                            div.appendChild(actions_report);

                            // display contact and remove button only if admin
                            if (admin) {
                                // emails are not transmitted if not admin, so we just hide button
                                let contactButton = document.createElement('a');
                                contactButton.href =
                                    'mailto:' + result[JSON_KEYS.get(FIELDS.UPLOADER)];
                                contactButton.classList.add('btn', 'btn-secondary', 'btn-sm');
                                contactButton.title = 'Contact uploader';
                                let contactButtonIcon = document.createElement('i');
                                contactButtonIcon.classList.add('bi', 'bi-envelope');
                                contactButton.appendChild(contactButtonIcon);
                                div.appendChild(contactButton);

                                // remove result button
                                let actions_delete = document.createElement('button');
                                actions_delete.type = 'button';
                                actions_delete.classList.add('btn', 'btn-danger', 'btn-sm');
                                actions_delete.addEventListener('click', function () {
                                    search_page.delete_result(result);
                                });
                                actions_delete.title = 'Delete';
                                let deleteButtonIcon = document.createElement('i');
                                deleteButtonIcon.classList.add('bi', 'bi-trash');
                                actions_delete.appendChild(deleteButtonIcon);
                                div.appendChild(actions_delete);
                            }
                            cell.appendChild(div);
                            row.appendChild(cell);
                        }
                        break;

                    // generic json-keypath column, just fetch data
                    default:
                        {
                            cell.textContent = _format_column_data(
                                fetch_subkey(result['data'], column)
                            );
                        }
                        break;
                }
                row.appendChild(cell);
            }

            this.table.appendChild(row);
        }
    }

    /**
     * Display a list of results.
     * @param results Results to display.
     * @param columns Columns to use.
     * @param startIndex The index of the first displayed item.
     */
    display(results, columns, startIndex) {
        this._clear();
        this._create_head(columns);
        this._fill_table(results, columns, startIndex);
    }

    /**
     * Set the column that is currently being sorted by
     * @param columnName the name of the column
     * @param order the order being used (SORT_ORDER)
     */
    set_column_sort(columnName, order) {
        let cell = this.columnHeads.get(columnName).element;
        // same column, reversed order
        if (order === Table.SORT_ORDER.REVERSED && this.sortedBy !== null) {
            // just reverse whatever order there was
            let arrow = cell.querySelector('.bi');
            if (arrow.classList.contains('bi-chevron-down')) {
                arrow.classList.remove('bi-chevron-down');
                arrow.classList.add('bi-chevron-up');
                this.sortReversed = true;
            } else {
                arrow.classList.add('bi-chevron-down');
                arrow.classList.remove('bi-chevron-up');
                this.sortReversed = false;
            }
            return;
        }

        // different column
        if (this.sortedBy !== null) {
            let arrow = this.columnHeads.get(this.sortedBy).element.querySelector('.bi');
            arrow.parentNode.removeChild(arrow);
        }

        let arrow = document.createElement('i');
        arrow.classList.add('bi', 'bi-chevron-down');
        cell.appendChild(arrow);

        this.sortedBy = columnName;
        this.sortReversed = false;
    }
}

Table.DEFAULT_COLUMNS = Object.freeze({
    CHECKBOX: 'Checkbox',
    BENCHMARK: FIELDS.BENCHMARK,
    SITE: FIELDS.SITE,
    FLAVOR: FIELDS.FLAVOR,
    TAGS: FIELDS.TAGS,
    ACTIONS: 'Actions',
});

// modes for sorting rows by column
Table.SORT_ORDER = Object.freeze({
    NONE: 0,
    NORMAL: 1,
    REVERSED: 2,
});

// JSON keys for the given table column
Table.COLUMN_KEYS = new Map([
    [Table.DEFAULT_COLUMNS.CHECKBOX, 'selected'],
    [Table.DEFAULT_COLUMNS.BENCHMARK, 'benchmark'],
    [Table.DEFAULT_COLUMNS.SITE, 'site'],
    [Table.DEFAULT_COLUMNS.FLAVOR, 'flavor'],
]);

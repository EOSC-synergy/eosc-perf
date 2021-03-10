"use strict";

const FIELDS = {
    BENCHMARK: 'Benchmark',
    SITE: 'Site',
    FLAVOR: 'Site flavour',
    TAGS: 'Tags',
    UPLOADER: 'Uploader'
};

const COLUMNS = {
    CHECKBOX: 'Checkbox',
    BENCHMARK: FIELDS.BENCHMARK,
    SITE: FIELDS.SITE,
    FLAVOR: FIELDS.FLAVOR,
    TAGS: FIELDS.TAGS,
    ACTIONS: 'Actions'
};

const FILTERS = {
    SITE: FIELDS.SITE,
    TAG: FIELDS.TAGS,
    UPLOADER: FIELDS.UPLOADER,
    JSON: "JSON-Key"
};

const FILTER_KEYS = new Map([
    [FILTERS.SITE, "site"],
    [FILTERS.TAG, "tag"],
    [FILTERS.UPLOADER, "uploader"],
    [FILTERS.JSON, "json"]
]);

const FILTER_HINTS = new Map([
    [FILTERS.SITE, "site identifier"],
    [FILTERS.TAG, "tag_name"],
    [FILTERS.UPLOADER, "user@example.com"],
    [FILTERS.JSON, "path.to.value"]
]);

const FILTER_HELPS = new Map([
    [FILTERS.SITE, "This field requires the site's identifier, which is a form of identifier. Sites can be found in the <i>Site</i> column in the result table below."],
    [FILTERS.TAG, "A tag is a short bit of text containing one or multiple keywords, such as <code>tensor</code> or <code>gpu_bound</code>."],
    [FILTERS.UPLOADER, "The Uploader is described by the uploader's email. Different uploaders can be found in the table below in the <i>Uploader</i> column."],
    [FILTERS.JSON, 'The search value has to describe the exact path within the JSON, separated with a dot.<br/>\
        <b>Example:</b><br/> \
        <code>{"example":{"nested":{"json":"value"},"different":{"path":{"to":"otherValue"}}}</code><br/> \
        <b>Correct:</b><br/> \
        example.nested.json or different.path.to \
        <b>Wrong:</b><br/> \
        json or example.nested or different:path:to']
]);

const JSON_MODES =  {
    LESS_THAN: 'lesser_than',
    LESS_OR_EQUALS: 'less_or_equals',
    EQUALS: 'equals',
    GREATER_OR_EQUALS: 'greater_or_equals',
    GREATER_THAN: 'greater_than'
};

const JSON_MODE_SYMBOLS = new Map([
    [JSON_MODES.LESS_THAN, '<'],
    [JSON_MODES.LESS_OR_EQUALS, '≤'],
    [JSON_MODES.EQUALS, '='],
    [JSON_MODES.GREATER_OR_EQUALS, '≥'],
    [JSON_MODES.GREATER_THAN, '>']
]);

const JSON_KEYS = new Map([
    [COLUMNS.BENCHMARK, "benchmark"],
    [COLUMNS.SITE, "site"],
    [COLUMNS.FLAVOR, "flavor"],
    [COLUMNS.TAGS, "tags"],
    [FIELDS.CHECKBOX, 'selected'],
    [FIELDS.UPLOADER, "uploader"],
]);

const CHART_COLORS = [
    'rgb(255, 99, 132)', // red
    'rgb(255, 159, 64)', // orange
    'rgb(255, 205, 86)', // yellow
    'rgb(75, 192, 192)', // green
    'rgb(54, 162, 235)', // blue
    'rgb(153, 102, 255)', // purple
    'rgb(201, 203, 207)' // gray
];

const SORT_ORDER = Object.freeze({
    NONE: 0,
    NORMAL: 1,
    REVERSED: 2,
});

const SUBKEY_NOT_FOUND = "⚠ not found";

/**
 * Fetch a sub-key from an object, as noted by the filter JSON syntax.
 * @param obj The object to get the value from.
 * @param key_path The path to the value.
 * @returns {*} Anything.
 * @private
 */
function _fetch_subkey(obj, key_path) {
    let keys = key_path.split('.');
    let sub_item = obj;
    for (let sub_key of keys) {
        if (typeof sub_item === "undefined") {
            console.error("Failed to fetch subkey", key_path, "from", obj);
            return SUBKEY_NOT_FOUND;
        }
        sub_item = sub_item[sub_key];
    }
    return sub_item;
}

/**
 * Get the name of the specific key accessed by a key-path of the filter JSON syntax.
 * @param key_path The path to the value.
 * @returns {*|string} The name of the specified key.
 * @private
 */
function _get_subkey_name(key_path) {
    let keys = key_path.split('.');
    return keys[keys.length - 1];
}

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
        return "⚠ not found";
    }
    if (typeof item === "number") {
        return (Math.round(item * 1000) / 1000).toString();
    }
    return item.toString();
}

/**
 * Get all attributes/keys from an object.
 * @param obj The object to get the keys from.
 * @returns {[]} The keys as a list.
 * @private
 */
function _keys_from_object(obj) {
    let keys = [];
    for (let key in obj) {
        keys.push(key);
    }
    return keys;
}

/**
 * Check if a keypath has valid syntax
 * @param key_path
 * @returns {boolean}
 * @private
 */
function _validate_keypath(key_path) {
    // alpha_num(.alpha_num)*
    return /^[\d\w_]+(\.[\d\w_]+)*$/.test(key_path);
}

/**
 * Clear all entries of a select dropdown.
 * @param selectElement The dropdown to remove options from.
 * @private
 */
function _clear_select(selectElement) {
    while (selectElement.firstChild) {
        selectElement.removeChild(selectElement.firstChild);
    }
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

/**
 * Helping wrapper to manage dropdown buttons for any needed json path input fields (filter suggestions, chart axis, ?)
 *
 * TODO: search field?
 */
class JSONValueInputPrompt {
    constructor(dropdownButton, inputBox) {
        this.button = dropdownButton;
        this.button.dataset.toggle = "dropdown";

        this.button.setAttribute("aria-haspopup", "true");
        this.button.setAttribute("aria-expanded", "false");

        this.inputBox = inputBox;

        this.dropdown = document.createElement("div");
        this.dropdown.classList.add("dropdown-menu", "dropdown-menu-right", "scrollable-dropdown");
        this.button.parentNode.insertBefore(this.dropdown, this.button);

        let jsonValueInputPrompt = this;
        // TODO: find better visual design than bootstrap list groups
        $(dropdownButton.parentElement).on('shown.bs.dropdown', function() {
            const keys = search_page.get_notable_keys();
            clear_element_children(jsonValueInputPrompt.dropdown);
            let list = document.createElement("ul");
            list.classList.add("list-group");
            for (const key of keys) {
                let item = document.createElement("li");
                item.textContent = key;
                item.classList.add("list-group-item");
                item.onclick = function () {
                    jsonValueInputPrompt.set_value(key);
                };
                list.appendChild(item);
            }
            jsonValueInputPrompt.dropdown.appendChild(list);
        });

        $(this.button).dropdown();
    }

    set_value(value) {
        this.inputBox.value = value;

        // call change callback if it exists
        if (this.inputBox.onchange !== undefined) {
            this.inputBox.onchange();
        }
    }
}

class Table {
    /**
     * Construct a new table handler.
     */
    constructor() {
        this.table = document.getElementById("result_table");
        this.columnHeads = new Map();
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
        // index 0 == table head
        let row = document.getElementById('table-entry-' + uuid);
        if (row === null) {
            return;
        }
        const childCount = row.children.length;
        clear_element_children(row);
        let shadow = document.createElement("td");
        shadow.classList.add("loading-background");
        shadow.style.opacity = "100%";
        let removedBadge = document.createElement("span");
        removedBadge.classList.add("badge", "bg-danger");
        removedBadge.textContent = "Removed";
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
    }

    /**
     * Set up the top row of the table.
     */
    _create_head(columns) {
        let table = this;
        let head = document.createElement("THEAD");
        for (const column of columns) {
            const column_name = (column in COLUMNS) ? COLUMNS[column] : _get_subkey_name(column);

            let cell = document.createElement("TH");
            this.columnHeads.set(column_name, {
                element: cell
            });

            if (!(column in COLUMNS)) {
                cell.dataset.toggle = "tooltip";
                cell.dataset.placement = "top";
                cell.title = column;
                if (column.includes(".")) {
                    cell.textContent = "(...)" + column_name;
                }
                else {
                    cell.textContent = column_name;
                }
            }
            else {
                // hide label for checkbox column because wide and redundant
                // TODO: compare against the enum directly somehow instead of magic "CHECKBOX" string
                if (column === "CHECKBOX") {
                    cell.textContent = "";
                }
                else {
                    cell.textContent = column_name;
                }
            }
            cell.scope = "col";

            switch (column_name) {
                case (COLUMNS.CHECKBOX): {
                    // sort by selected results
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => _comparator(x["selected"], y["selected"]), column_name);
                    });
                }
                    break;
                case (COLUMNS.BENCHMARK): {
                    // alphabetically sort by benchmark
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => _comparator(x["benchmark"], y["benchmark"]), column_name);
                    });
                }
                    break;
                case (COLUMNS.SITE): {
                    // alphabetically sort by site
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => _comparator(x["site"], y["site"]), column_name);
                    });
                }
                    break;
                case (COLUMNS.FLAVOR): {
                    // alphabetically sort by site flavor
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => _comparator(x["flavor"], y["flavor"]), column_name);
                    });
                }
                    break;
                case (COLUMNS.UPLOADER): {
                    // alphabetically sort by uploader
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => _comparator(x["uploader"], y["uploader"]), column_name);
                    });
                }
                    break;
                case (COLUMNS.TAGS):
                    // todo find order on tags
                    break;
                default:
                    cell.addEventListener("click", function() {
                        // TODO: sorting helpers
                        search_page.sort_by( (x, y) => _comparator(_fetch_subkey(x["data"], column), _fetch_subkey(y["data"], column)), column_name);
                    });
                    break;
            }

            if (this.sortedBy === column_name) {
                let arrow = document.createElement("i");
                arrow.classList.add("bi");
                if (this.sortReversed) {
                    arrow.classList.add("bi-chevron-up");
                }
                else {
                    arrow.classList.add("bi-chevron-down");
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
            let row = document.createElement("TR");
            const result = results[i];
            row.id = 'table-entry-' + result.uuid;

            for (const key of columns) {
                const column = (key in COLUMNS) ? COLUMNS[key] : key;
                let cell = document.createElement("TD");
                switch (column) {
                    case (COLUMNS.CHECKBOX): {
                        let select = document.createElement("input");
                        select.type = "checkbox";
                        select.id = "selected" + i;
                        if (result[JSON_KEYS.get(FIELDS.CHECKBOX)]) {
                            select.checked = true;
                        }
                        select.style.height = "1.5em";
                        // when clicked, select
                        select.addEventListener("click", function () {
                            search_page.select_result(i + startIndex);
                        });
                        cell.appendChild(select);
                    } break;

                    case (COLUMNS.FLAVOR):
                    case (COLUMNS.SITE):
                    case (COLUMNS.BENCHMARK): {
                        cell.textContent = result[JSON_KEYS.get(column)];
                    } break;

                    case (COLUMNS.TAGS): {
                        const content = result[JSON_KEYS.get(column)];
                        if (content.length === 0) {
                            cell.textContent = "None";
                            cell.style.color = "#9F9F9F";
                        }
                        else {
                            cell.textContent = content;
                        }
                    } break;

                    case COLUMNS.ACTIONS: {
                        // actions
                        let div = document.createElement('div');
                        div.classList.add('btn-group');

                        let view_button = document.createElement("button");
                        view_button.type = "button";
                        view_button.classList.add("btn", "btn-primary", "btn-sm");
                        view_button.addEventListener("click", function () {
                            search_page.display_result(result);
                        });
                        view_button.title = "View JSON";
                        let viewButtonIcon = document.createElement("i");
                        viewButtonIcon.classList.add("bi", "bi-hash");
                        view_button.appendChild(viewButtonIcon);
                        div.appendChild(view_button);

                        let actions_report = document.createElement("button");
                        actions_report.type = "button";
                        actions_report.classList.add('btn', 'btn-warning', 'btn-sm');
                        actions_report.addEventListener('click', function () {
                            search_page.report_result(result);
                        });
                        actions_report.title = "Report";
                        let reportButtonIcon = document.createElement("i");
                        reportButtonIcon.classList.add("bi", "bi-exclamation");
                        actions_report.appendChild(reportButtonIcon);
                        div.appendChild(actions_report);

                        // display contact and remove button only if admin
                        if (admin) {
                            // emails are not transmitted if not admin, so we just hide button
                            let contactButton = document.createElement("a");
                            contactButton.href = "mailto:" + result[JSON_KEYS.get(FIELDS.UPLOADER)];
                            contactButton.classList.add("btn", "btn-secondary", "btn-sm");
                            contactButton.title = "Contact uploader";
                            let contactButtonIcon = document.createElement("i");
                            contactButtonIcon.classList.add("bi", "bi-envelope");
                            contactButton.appendChild(contactButtonIcon);
                            div.appendChild(contactButton);

                            let actions_delete = document.createElement('button');
                            actions_delete.type = "button";
                            actions_delete.classList.add('btn', 'btn-danger', 'btn-sm');
                            actions_delete.addEventListener('click', function () {
                                search_page.delete_result(result);
                            });
                            actions_delete.title = "Delete";
                            let deleteButtonIcon = document.createElement("i");
                            deleteButtonIcon.classList.add("bi", "bi-trash");
                            actions_delete.appendChild(deleteButtonIcon);
                            div.appendChild(actions_delete);
                        }
                        cell.appendChild(div);
                        row.appendChild(cell);
                    } break;

                    default: {
                        cell.textContent = _format_column_data(_fetch_subkey(result["data"], column));
                    } break;
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

    set_column_sort(columnName, order) {
        let cell = this.columnHeads.get(columnName).element;
        // same column, reversed order
        if (order === SORT_ORDER.REVERSED && this.sortedBy !== null) {
            // just reverse whatever order there was
            let arrow = cell.querySelector(".bi");
            if (arrow.classList.contains("bi-chevron-down")) {
                arrow.classList.remove("bi-chevron-down");
                arrow.classList.add("bi-chevron-up");
                this.sortReversed = true;
            }
            else {
                arrow.classList.add("bi-chevron-down");
                arrow.classList.remove("bi-chevron-up");
                this.sortReversed = false;
            }
            return;
        }

        // different column
        if (this.sortedBy !== null) {
            let arrow = this.columnHeads.get(this.sortedBy).element.querySelector(".bi");
            arrow.parentNode.removeChild(arrow);
        }

        let arrow = document.createElement("i");
        arrow.classList.add("bi", "bi-chevron-down");
        cell.appendChild(arrow);

        this.sortedBy = columnName;
        this.sortReversed = false;
    }
}

class PageNavigation {
    /**
     * Set up page navigation handler.
     */
    constructor() {
        this.current_page = 0;
        this.results_per_page = 10;
        this.page_count = 1;
        this.result_count = 0;
    }

    /**
     * Update pagination buttons.
     */
    update() {
        // clear away all page buttons
        let it = document.getElementById('prevPageButton');
        it = it.nextElementSibling;
        while (it.id !== 'nextPageButton') {
            let it_next = it.nextElementSibling;
            it.parentElement.removeChild(it);
            it = it_next;
        }
        // (re-)add them
        let next_page_button = document.getElementById('nextPageButton');
        for (let i = 0; i < this.page_count; i++) {
            // link box
            let new_page_link_slot = document.createElement('li');
            new_page_link_slot.classList.add('page-item');
            // page link button
            let new_page_link = document.createElement('a');
            new_page_link.textContent = (i + 1).toString();
            new_page_link.classList.add('page-link');
            new_page_link.addEventListener("click", function() {
                search_page.get_paginator().set_page(i);
            });
            // highlight current page
            if (i === this.current_page) {
                new_page_link_slot.classList.add('active');
            }
            new_page_link_slot.appendChild(new_page_link);
            it.parentElement.insertBefore(new_page_link_slot, next_page_button);
        }

        if (this.current_page === 0) {
            document.getElementById("prevPageButton").classList.add('disabled');
        }
        else {
            document.getElementById("prevPageButton").classList.remove('disabled');
        }
        if (this.current_page === this.page_count - 1) {
            document.getElementById("nextPageButton").classList.add('disabled');
        }
        else {
            document.getElementById("nextPageButton").classList.remove('disabled');
        }
    }

    /**
     * Update the number of pages
     */
    update_page_count() {
        this.page_count = Math.max(Math.ceil(this.result_count / this.results_per_page), 1);
        if (this.current_page >= this.page_count) {
            this.current_page = this.page_count - 1;
        }
    }

    /**
     * Update the current number of results.
     * @param result_count The new number of results.
     */
    set_result_count(result_count) {
        this.result_count = result_count;
        this.update_page_count();
        this.update();
    }

    /**
     * Go to the previous page.
     */
    prev_page() {
        this.current_page = Math.max(0, this.current_page - 1);
        this.update();
        search_page.update();
    }

    /**
     * Go to the specified page.
     * @param page page number
     */
    set_page(page) {
        this.current_page = Math.max(0, Math.min(page, this.page_count - 1));
        this.update();
        search_page.update();
    }

    /**
     * Go to the previous page.
     */
    next_page() {
        this.current_page = Math.min(this.page_count - 1, this.current_page + 1);
        this.update();
        search_page.update();
    }

    /**
     * Get the index of the first result displayed on page.
     * @returns {number} The index of the first result displayed on page.
     */
    get_start_index() {
        return this.current_page * this.results_per_page;
    }

    /**
     * Get the index of one past the last result displayed on page.
     * @returns {number} The index of one past the last result displayed on page.
     */
    get_end_index() {
        return (this.current_page + 1) * this.results_per_page;
    }

    /**
     * Update the number of results displayed per page.
     */
    update_page_result_count() {
        this.results_per_page = document.getElementById("results_on_page").value;
        // Restart at page 1;
        this.current_page = 0;
        this.update_page_count();
        this.update();
        search_page.update();
    }
}

class Diagram {
    update_notable_keys(notable_keys) {
    }
    updateData(results) {
    }
    cleanup() {
    }
    update_diagram_configuration() {
    }
}

class SpeedupDiagram extends Diagram {
    /**
     * Build a new speedup diagram
     */
    constructor() {
        super();
        this.results = [];
        this.xAxis = "";
        this.yAxis = "";
        this.notable_keys = [];
        this.mode = "simple";
        this.grouping = false;

        document.getElementById("diagramConfiguration-speedup").classList.remove("d-none");

        let section = document.getElementById("diagramSection");
        {
            let xAxisDiv = document.createElement("div");
            xAxisDiv.classList.add("form-inline");
            {
                let label = document.createElement("label");
                label.for = "diagramX";
                label.textContent = "X Axis:";
                label.style.paddingRight = "0.2em";
                xAxisDiv.appendChild(label);

                let inputGroup = document.createElement("div");
                inputGroup.classList.add("input-group");

                this.xAxisInput = document.createElement("input");
                this.xAxisInput.type = "text";
                this.xAxisInput.placeholder = "path.to.value";
                this.xAxisInput.classList.add("form-control");
                this.xAxisInput.onchange = function() {
                    search_page.get_diagram()._update();
                };
                inputGroup.appendChild(this.xAxisInput);

                let inputGroupAppend = document.createElement("div");
                inputGroupAppend.classList.add("input-group-append");

                let xAxisDropdownButton = document.createElement("button");
                xAxisDropdownButton.classList.add("btn", "btn-outline-secondary", "dropdown-toggle", "dropdown-toggle-split");
                inputGroupAppend.appendChild(xAxisDropdownButton);
                this.xAxisJsonSelector = new JSONValueInputPrompt(xAxisDropdownButton, this.xAxisInput);

                inputGroup.appendChild(inputGroupAppend);
                xAxisDiv.appendChild(inputGroup);

            }
            section.appendChild(xAxisDiv);

            let yAxisDiv = document.createElement("div");
            yAxisDiv.classList.add("form-inline");
            {
                let label = document.createElement("label");
                label.for = "diagramY";
                label.textContent = "Y Axis:";
                label.style.paddingRight = "0.2em";
                yAxisDiv.appendChild(label);

                let inputGroup = document.createElement("div");
                inputGroup.classList.add("input-group");

                this.yAxisInput = document.createElement("input");
                this.yAxisInput.type = "text";
                this.yAxisInput.placeholder = "path.to.value";
                this.yAxisInput.classList.add("form-control");
                this.yAxisInput.onchange = function() {
                    search_page.get_diagram()._update();
                };
                inputGroup.appendChild(this.yAxisInput);

                let inputGroupAppend = document.createElement("div");
                inputGroupAppend.classList.add("input-group-append");

                let yAxisDropdownButton = document.createElement("button");
                yAxisDropdownButton.classList.add("btn", "btn-outline-secondary", "dropdown-toggle", "dropdown-toggle-split");
                inputGroupAppend.appendChild(yAxisDropdownButton);
                this.yAxisJsonSelector = new JSONValueInputPrompt(yAxisDropdownButton, this.yAxisInput);

                inputGroup.appendChild(inputGroupAppend);
                yAxisDiv.appendChild(inputGroup);

            }
            section.appendChild(yAxisDiv);

            let canvas = document.createElement("canvas");
            canvas.id = "speedup";
            section.appendChild(canvas);

            let interactions = document.createElement("div");
            {
                let downloadButton = document.createElement("button");
                downloadButton.id = "downloadButton";
                downloadButton.type = "button";
                downloadButton.classList.add("btn", "btn-light");
                downloadButton.textContent = "Download as PNG";
                downloadButton.onclick = function() {
                    search_page.get_diagram().downloadPNG();
                };
                interactions.appendChild(downloadButton);

                let csvButton = document.createElement("button");
                csvButton.id = "csvButton";
                csvButton.type = "button";
                csvButton.classList.add("btn", "btn-light");
                csvButton.textContent = "Download as CSV";
                csvButton.onclick = function() {
                    search_page.get_diagram().downloadCSV();
                };
                interactions.appendChild(csvButton);
            }
            section.appendChild(interactions);
        }
    }

    /**
     * Pass various checks over the used data to verify if certain diagrams are viable.
     *
     * sameSite: all results are from the same site
     * columnsAreNumbers: all columns/labels are actual numbers and can for example be put on a log scale
     *
     * @returns {{sameSite: boolean, columnsAreNumbers: boolean}}
     * @private
     */
    _determineDataProperties() {
        let sameSite = true;
        let columnsAreNumbers = true;

        // test if sites are the same all across and if it's an integer range
        if (this.results.length !== 0) {
            const site_path = JSON_KEYS.get(COLUMNS.SITE);
            let siteName = _fetch_subkey(this.results[0], site_path);
            for (const result of this.results) {
                sameSite &&= (_fetch_subkey(result, site_path) === siteName);
                columnsAreNumbers &&= typeof _fetch_subkey(result.data, this.xAxis) === 'number';
            }
        }
        else {
            sameSite = false;
            columnsAreNumbers = false;
        }

        return {
            sameSite, columnsAreNumbers
        };
    }

    /**
     * Build a chart.js dataset off current data
     *
     * TODO: add nulls for columns this dataset has no value for
     *
     * @returns {{data: [{spanGaps: boolean, backgroundColor: *, borderColor: string|string, data: [], borderWidth: number, label: *|string}], labels: []}}
     * @private
     */
    _generateChartData(properties) {
        let labels = []; // labels below graph
        let dataPoints = [];
        let color = Chart.helpers.color;

        // grouping-by-site behaviour
        if (this.grouping === true && (this.mode === "linear" || this.mode === "log")) {
            let datasets = new Map();
            let labelSet = new Set();

            for (const result of this.results) {
                const x = _fetch_subkey(result.data, this.xAxis);
                const y = _fetch_subkey(result.data, this.yAxis);
                let label = x.toString();
                if (datasets.get(result.site) === undefined) {
                    datasets.set(result.site, []);
                }
                datasets.get(result.site).push({x, y});
                dataPoints.push({x, y});
                labelSet.add(label);
            }

            let data = [];
            let colorIndex = 0;
            datasets.forEach(function(dataset, site, map) {
                data.push({
                    label: site,
                    backgroundColor: color(CHART_COLORS[colorIndex]).alpha(0.5).rgbString(),
                    borderColor: CHART_COLORS[colorIndex],
                    borderWidth: 1,
                    data: dataset,
                    spanGaps: true
                });
                colorIndex++;
            });

            return {
                labels: Array.from(labelSet).sort(),
                data: data
            };
        }

        // default behaviour
        for (const result of this.results) {
            const x = _fetch_subkey(result.data, this.xAxis);
            const y = _fetch_subkey(result.data, this.yAxis);
            let label = x.toString();
            if (!properties.sameSite) {
                label += ' (' + _fetch_subkey(result, JSON_KEYS.get(COLUMNS.SITE)) + ')';
            }
            dataPoints.push({x, y});
            labels.push(label);
        }

        return {
            labels: labels,
            data: [{
                label: _get_subkey_name(this.yAxis),
                backgroundColor: color(CHART_COLORS[0]).alpha(0.5).rgbString(),
                borderColor: CHART_COLORS[0],
                borderWidth: 1,
                data: dataPoints,
                spanGaps: true
            }]
        }
    }

    /**
     * Download a csv file off current data
     */
    downloadCSV() {
        let download = document.createElement("a");
        let dataHeader = "data:text/csv;charset=utf-8,";
        let rows = [this.xAxis + "," + this.yAxis + ",site"];
        for (const row of this.results) {
            let x = _fetch_subkey(row.data, this.xAxis);
            let y = _fetch_subkey(row.data, this.yAxis);
            let site = _fetch_subkey(row, JSON_KEYS.get(COLUMNS.SITE));
            rows.push(x.toString() + "," + y.toString() + "," + site.toString());
        }
        download.href = encodeURI(dataHeader + rows.join("\r\n"));
        download.download = "data.csv";
        download.click();
    }

    /**
     * Download a picture copy of the current diagram
     */
    downloadPNG() {
        let download = document.createElement("a");
        let context = document.getElementById('speedup');
        download.href = context.toDataURL('image/png');
        download.download = "diagram.png";
        download.click();
    }

    /**
     * Update the array of notable keys.
     * @param notable_keys The notable keys to make selectable for axis.
     */
    update_notable_keys(notable_keys) {
        this.notable_keys = notable_keys;

        // pick something by default
        this.xAxisInput.value = notable_keys[0];
        this.yAxisInput.value = notable_keys[0];
    }

    /**
     * Update diagram chart
     */
    refresh() {
        let { labels: labels, data: dataSets } = this._generateChartData(this.properties);

        if (window.diagram !== undefined && window.diagram !== null) {
            window.diagram.data.labels = labels;
            window.diagram.data.datasets = dataSets;

            window.diagram.options.scales.yAxes[0].scaleLabel.labelString = this.yAxis;
            window.diagram.options.scales.xAxes[0].scaleLabel.labelString = this.xAxis;

            if (this.mode === "log") {
                window.diagram.options.scales.xAxes[0].type = 'logarithmic';
                window.diagram.options.scales.yAxes[0].type = 'logarithmic';
            }
            else if (this.mode === "linear") {
                window.diagram.options.scales.xAxes[0].type = 'linear';
                window.diagram.options.scales.yAxes[0].type = 'linear';
            }
            else /* simple */ {
                delete window.diagram.options.scales.xAxes[0].type;
                window.diagram.options.scales.yAxes[0].type = 'linear';
            }

            window.diagram.update();
        }
        else {
            let context = document.getElementById('speedup').getContext('2d');
            let configuration = {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: dataSets,
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Line Graph'
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            },
                            scaleLabel: {
                                display: true,
                                labelString: this.yAxis
                            }
                        }],
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: this.xAxis
                            }
                        }]
                    },
                    elements: {
                        line: {
                            tension: 0
                        }
                    },
                    tooltips: {
                        callbacks: {
                            title: function(tooltipItem, entry) {
                                return tooltipItem[0].yLabel + ' (' + tooltipItem[0].label + ')';
                            }
                        }
                    }
                }
            };
            if (this.mode === "log") {
                configuration.options.scales.xAxes[0].type = 'logarithmic';
                configuration.options.scales.yAxes[0].type = 'logarithmic';
            }
            else if (this.mode === "linear") {
                configuration.options.scales.xAxes[0].type = 'linear';
                configuration.options.scales.yAxes[0].type = 'linear';
            }
            else /* simple */ {
                delete configuration.options.scales.xAxes[0].type;
                configuration.options.scales.yAxes[0].type = 'linear';
            }
            window.diagram = new Chart(context, configuration);
        }

        document.getElementById("downloadButton").disabled = false;
        document.getElementById("csvButton").disabled = false;
    }

    _update() {
        this.xAxis = this.xAxisInput.value;
        this.yAxis = this.yAxisInput.value;

        this.properties = this._determineDataProperties();

        if (this.properties.sameSite) {
            document.getElementById("speedupDiagramMode").children.namedItem("speedupDiagramMode-linear").disabled = !this.properties.columnsAreNumbers;
            document.getElementById("speedupDiagramMode").children.namedItem("speedupDiagramMode-log").disabled = !this.properties.columnsAreNumbers;
        }

        if (this.properties.columnsAreNumbers === false && (this.mode === "log" || this.mode === "linear")) {
            this.mode = "simple";
            document.getElementById("speedupDiagramMode").value = "simple";
        }

        if (!_validate_keypath(this.xAxis) || !_validate_keypath(this.yAxis) || this.results.length === 0) {
            document.getElementById("downloadButton").disabled = "true";
            document.getElementById("csvButton").disabled = "true";
            document.getElementById("speedup").style.display = "none";
            return;
        }
        else {
            document.getElementById("speedup").style.removeProperty("display");
        }

        this.refresh();
    }

    /**
     * Update diagram data
     * @param data The new results to use.
     */
    updateData(data) {
        this.results = data;

        this._update();
    }

    /**
     * Remove data associated to this component, such as chart.js objects and HTML elements.
     */
    cleanup() {
        if (window.diagram) {
            window.diagram.destroy();
            delete window.diagram;
        }

        document.getElementById("diagramConfiguration-speedup").classList.add("d-none");

        // naïve purge
        _clear_select(document.getElementById("diagramSection"));
    }

    update_diagram_configuration() {
        this.mode = document.getElementById("speedupDiagramMode").value;
        this.grouping = document.getElementById("speedupDiagramGroupedMode").checked;
        this._update();
    }
}

class Filter {
    constructor(searchPage) {
        this.searchPage = searchPage;

        // add line for the filter
        this.element = document.createElement('li');
        this.element.classList.add("form-inline");

        // Remove this filter
        let deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.classList.add("close");
        deleteButton.setAttribute("aria-label", "Close");
        // label
        {
            let remove_filter_label = document.createElement("span");
            remove_filter_label.setAttribute("aria-hidden", "true");
            remove_filter_label.textContent = "×";
            deleteButton.appendChild(remove_filter_label);
        }
        let filter = this;
        deleteButton.addEventListener("click", function () {
            filter.remove();
        });
        this.element.appendChild(deleteButton);

        // filter type selection
        this.filterType = document.createElement("select");
        for (let filter in FILTERS) {
            // skip uploader filter option if not admin
            if (filter === "UPLOADER" && !isAdmin()) {
                continue;
            }
            let type = document.createElement("OPTION");
            type.value = FILTERS[filter];
            type.textContent = FILTERS[filter];
            this.filterType.appendChild(type);
        }
        this.element.appendChild(this.filterType);

        // On change callback
        this.filterType.addEventListener("change", function () {
            filter.inputBox.placeholder = FILTER_HINTS.get(filter.filterType.value);
            filter.jsonTypeHelp.dataset.content = FILTER_HELPS.get(filter.filterType.value);

            // hide extra json input on other filters
            filter.suggestionsButton.disabled = true;
            filter.extraJsonInput.style.visibility = "hidden";
            if (filter.filterType.value.localeCompare(FILTERS.JSON) === 0) {
                filter.suggestionsButton.disabled = false;
                filter.extraJsonInput.style.visibility = "visible";
            }
        });
        this.filterType.classList.add("custom-select");

        // Primary input
        let input = document.createElement("div");
        input.classList.add("input-group");
        // textbox
        this.inputBox = document.createElement("input");
        this.inputBox.type = "text";
        this.inputBox.placeholder = "Filter Value";
        this.inputBox.classList.add("form-control");
        input.appendChild(this.inputBox);

        // suggestions & info
        {
            let inputExtras = document.createElement("div");
            inputExtras.classList.add("input-group-append");

            // Info button
            {
                this.jsonTypeHelp = document.createElement("input");
                this.jsonTypeHelp.type = "button";
                this.jsonTypeHelp.classList.add("btn", "btn-outline-warning");
                this.jsonTypeHelp.value = "?";
                this.jsonTypeHelp.dataset.toggle = "popover";
                this.jsonTypeHelp.title = "Format Description";
                this.jsonTypeHelp.dataset.content = "You find some Tips for the expected input values here.";
                this.jsonTypeHelp.dataset.placement = "right";
                inputExtras.appendChild(this.jsonTypeHelp);
            }

            {
                this.suggestionsButton = document.createElement("button");
                this.suggestionsButton.disabled = true;
                this.suggestionsButton.classList.add("btn", "btn-outline-secondary", "dropdown-toggle", "dropdown-toggle-split");

                {
                    let suggestions_button_screenreader_hint = document.createElement("span");
                    suggestions_button_screenreader_hint.classList.add("sr-only");
                    suggestions_button_screenreader_hint.textContent = "Toggle Dropdown";
                    this.suggestionsButton.appendChild(suggestions_button_screenreader_hint);
                }
                inputExtras.appendChild(this.suggestionsButton);
                this.jsonSuggestor = new JSONValueInputPrompt(this.suggestionsButton, this.inputBox);
            }

            input.appendChild(inputExtras);
        }
        this.element.appendChild(input);

        // Extra JSON input
        this.extraJsonInput = document.createElement("div");
        this.extraJsonInput.classList.add("input-group");
        this.extraJsonInput.style.visibility = "hidden";
        // comparison mode dropdown
        {
            let jsonMode = document.createElement("div");
            jsonMode.classList.add("input-group-prepend");
            {
                this.jsonModeButton = document.createElement("button");
                this.jsonModeButton.classList.add("btn", "btn-outline-secondary", "dropdown-toggle");
                this.jsonModeButton.type = "button";
                this.jsonModeButton.dataset.toggle = "dropdown";
                this.jsonModeButton.setAttribute("aria-haspopup", "true");
                this.jsonModeButton.setAttribute("aria-expanded", "false");
                this.jsonModeButton.value = JSON_MODES.GREATER_THAN;
                this.jsonModeButton.textContent = JSON_MODE_SYMBOLS.get(JSON_MODES.GREATER_THAN);
                jsonMode.appendChild(this.jsonModeButton);

                let jsonModeDropdown = document.createElement("div");
                jsonModeDropdown.classList.add("dropdown-menu");
                for (let mode in JSON_MODES) {
                    mode = JSON_MODES[mode];
                    let jsonModeOption = document.createElement("a");
                    jsonModeOption.classList.add("dropdown-item");
                    jsonModeOption.value = mode;
                    jsonModeOption.textContent = JSON_MODE_SYMBOLS.get(mode);
                    jsonModeOption.addEventListener("click", function() {
                        filter.jsonModeButton.value = mode;
                        filter.jsonModeButton.textContent = JSON_MODE_SYMBOLS.get(mode);
                    });
                    jsonModeDropdown.appendChild(jsonModeOption);
                }
                jsonMode.appendChild(jsonModeDropdown);
            }
            this.extraJsonInput.appendChild(jsonMode);
        }
        // json value input
        {
            this.jsonValue = document.createElement("input");
            this.jsonValue.classList.add("form-control");
            this.extraJsonInput.appendChild(this.jsonValue);
        }
        this.element.appendChild(this.extraJsonInput);

        document.getElementById('filters').appendChild(this.element);

        // prepare initial contents as if user just selected it
        let changeEvent = document.createEvent("HTMLEvents");
        changeEvent.initEvent("change", false, true);
        this.filterType.dispatchEvent(changeEvent);

        // Activate popover.
        $(this.element).popover({
            html: true
        });

    }

    remove() {
        this.element.parentNode.removeChild(this.element);
        this.searchPage.remove_filter(this);
    }

    getType() {
        return this.filterType.value;
    }

    getValue() {
        return this.inputBox.value;
    }

    getJsonMode() {
        return this.jsonModeButton.value;
    }

    getJsonValue() {
        return this.jsonValue.value;
    }
}

/**
 * The ResultSearch class is responsible to communicate with the backend to get the search results and display them.
 * TODO: split into smaller parts
 */
class ResultSearch {
    /**
     * Set up result search.
     */
    constructor() {
        this.results = [];
        this.filters = [];
        this.ordered_by = null;
        this.current_filter_id = 0;
        this.filters = [];
        this.notable_keys = [];

        this.active_columns = [];
        this._populate_active_columns();

        this.table = new Table();
        this.paginator = new PageNavigation();

        this.benchmark_name = "";

        this.diagram = null;
    }

    /**
     * Function called on page load.
     */
    onload() {
        // Case it got initialed with a Benchmark.
        this.fetch_all_benchmarks(true);
        // in case page was refreshed and something was auto-selected by the browser
        // this can't be done for benchmarks for now because the list is re-populated every load
        this.select_diagram_type();
        this.add_filter_field();
        // Enable popover.
        $('[data-toggle="popover"]').popover({
            html: true
        });
    }

    /**
     * Update the view.
     */
    update() {
        // Update table.
        let start = this.paginator.get_start_index();
        let end = Math.min(this.paginator.get_end_index(), this.results.length);
        this.table.display(this.results.slice(start, end), this.active_columns, start);

        if (this.diagram !== null) {
            this.diagram.updateData(this.get_selected_results());
        }

        $('[data-toggle="popover"]').popover({
            html: true
        });

        $('[data-toggle="tooltip"]').tooltip();
    }

    /**
     * Display the specified result in a popup.
     * @param result The result to display.
     */
    display_result(result) {
        document.getElementById('jsonPreviewContent').textContent = JSON.stringify(result.data, null, 4);
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block);
        });
        $('#jsonPreviewModal').modal('show');
    }

    /**
     * Get the current amount of results.
     * @returns {number} The current amount of results.
     */
    get_result_count() {
        return this.results.length;
    }

    /**
     * Execute a new search query.
     * @returns {boolean} false (skip other event handlers)
     */
    search() {
        /** Search the database using selected filters. */
        // Generate query.
        let filters = [];
        if (this.benchmark_name !== '') {
            filters.push({
                'type': 'benchmark',
                'value': this.benchmark_name
            });
        }

        for (let filter of this.filters) {
            let filterInfo = {};
            const filterType = filter.getType();
            const value = filter.getValue();

            filterInfo['type'] = FILTER_KEYS.get(filterType);
            if (filterType.toString().localeCompare(FILTERS.JSON) === 0) {
                const jsonValue = filter.getJsonValue();
                filterInfo['value'] = jsonValue;
                filterInfo['key'] = filter.getValue();
                filterInfo['mode'] = filter.getJsonMode();
                if (value && jsonValue) {
                    filters.push(filterInfo);
                }
            }
            else {
                filterInfo['value'] = value;
                if (value) {
                    filters.push(filterInfo);
                }
            }
        }

        // Finish query.
        let query = { "filters": filters };

        document.getElementById('loading-icon').classList.add('loading');

        // Find get new results via ajax query.
        $.ajax('/query_results?query_json=' + encodeURI(JSON.stringify(query)))
            .fail(function (jqXHR, textStatus, errorThrown) {
                if (jqXHR.status === 401) {
                    // unauthorized query (uploader)
                    // TODO: how should we display error messages inline? popup? toast?
                }
                search_page.results = [];
                console.error("Error", jqXHR.status, "occured while searching searching");
            })
            .done(function (data) {
                if (!data.hasOwnProperty("results")) {
                    console.error("Search page returned no data!");
                    return;
                }
                search_page.results = data["results"];
                if (search_page.results.length > 0) {
                    // add selected col
                   search_page.results.forEach(element => {
                        element[JSON_KEYS.get(FIELDS.CHECKBOX)] = false;
                    });
                }
            }).always(function () {
                search_page.current_page = 1;
                search_page.get_paginator().set_result_count(search_page.get_result_count());
                search_page.update();
                document.getElementById('loading-icon').classList.remove('loading');
            });
        return false;
    }

    /**
     * Add a filter field.
     */
    add_filter_field() {
        this.filters.push(new Filter(this));
    }

    /**
     * Remove a filter field.
     * @param filter The filter to remove.
     */
    remove_filter(filter) {
        const index = this.filters.indexOf(filter);
        if (index > -1) {
            this.filters.splice(index, 1);
        }
        else {
            console.error("Failed to remove filter from internal filter list!");
        }
    }

    /**
     * Sort the results by a given column.
     * @param callback Comparison function for the sort.
     * @param column Which column to sort by.
     */
    sort_by(callback, column) {
        // reverse order if double clicked.
        if (this.ordered_by === column) {
            this.results = this.results.reverse();
            this.table.set_column_sort(column, SORT_ORDER.REVERSED);
        }
        else {
            this.results.sort(callback);
            this.table.set_column_sort(column, SORT_ORDER.NORMAL);
        }
        this.ordered_by = column;
        this.update();
        // remove possible column hover tooltips
        $('.tooltip').remove();
    }

    /**
     * Select a specific result.
     * @param result_number The index of the result to select.
     */
    select_result(result_number) {
        this.results[result_number][JSON_KEYS.get(FIELDS.CHECKBOX)] ^= true;
        if (this.diagram !== null) {
            this.diagram.updateData(this.get_selected_results());
        }
    }

    /**
     * Open a URL in a new tab.
     * @param url URL to open in a new tab.
     */
    open_new_tab(url) {
        window.open(url, '_blank');
    }

    /**
     * Report a given result.
     * @param result The result to report.
     */
    report_result(result) {
        this.open_new_tab('./report_result' + '?uuid=' + result['uuid']);
    }

    /**
     * Delete a given result.
     * @param result The result to delete.
     * @returns {boolean} false (skip other event listener)
     */
    delete_result(result) {
        $.ajax('/delete_result?uuid=' + encodeURI(result['uuid'])).done(function (data) {
            if (data.toLowerCase().includes("success")) {
                search_page.table.mark_result_as_removed(result.uuid);
                search_page.results = search_page.results.filter(function (r) {
                    return r.uuid !== result.uuid;
                });
            }
            else {
                alert("Could not remove result!");
            }
        });
        return false;
    }

    /**
     * Invert the current result selection
     * @returns {boolean} false (skip other event listener)
     */
    selection_invert() {
        if(this.results.length === 0) {
            return false;
        }
        this.results.forEach(r => {
            r.selected = !r.selected;
        });
        this.update();
        return false;
    }

    /**
     * Select all results
     * @returns {boolean} false (skip other event listener)
     */
    selection_all() {
        if(this.results.length === 0) {
            return false;
        }
        this.results.forEach(r => {
            r.selected = true;
        });
        this.update();
        return false;
    }

    /**
     * Set the named benchmark to the active one.
     * @param benchmark_name The name of the benchmark to set as active.
     */
    set_benchmark(benchmark_name) {
        this.benchmark_name = benchmark_name;
        let selection = document.getElementById("benchmark_selection");
        for (let i = 0; i < selection.options.length; i++) {
            if (selection.options[i].value.localeCompare(benchmark_name) === 0) {
                selection.selectedIndex = i;
            }
        }

        if (benchmark_name.length > 0) {
            this._poll_notable_keys(benchmark_name);

            let infoButton = document.getElementById("dockerhubLinkButton");
            infoButton.onclick = function() {
                open_tab("https://hub.docker.com/r/" + benchmark_name.split(':')[0]);
            };
            infoButton.disabled = false;

            this._enable_diagram_selection();
        }
        else {
            this.set_notable_keys([]);
            document.getElementById("dockerhubLinkButton").disabled = true;

            this._disable_diagram_selection();
        }
    }

    /**
     * Callback for benchmark selection dropdown.
     */
    update_benchmark_selection() {
        let selected_benchmark = document.getElementById("benchmark_selection").value;
        this.set_benchmark(selected_benchmark);
        this.search();
    }

    /**
     * Fill active column list with all default columns and notable keys
     * @private
     */
    _populate_active_columns() {
        for (let column in COLUMNS) {
            this.active_columns.push(column);
        }
        for (let field of this.notable_keys) {
            this.active_columns.push(field);
        }
    }

    /**
     * Set the list of notable keys regarding the current benchmark.
     * @param keys The list of notable keys.
     */
    set_notable_keys(keys) {
        this.notable_keys = keys;

        this.active_columns = [];
        this._populate_active_columns();

        this.update();

        if (this.diagram !== null) {
            this.diagram.update_notable_keys(this.notable_keys);
        }
    }

    /**
     * Get an array of all the notable keys
     * @returns {[]} an array of "json.value.path" structured paths
     */
    get_notable_keys() {
        return this.notable_keys;
    }

    /**
     * Get a list of all benchmarks from the server.
     * @param first_run True if this is on page load.
     */
    fetch_all_benchmarks(first_run = false) {
        $.ajax('/fetch_benchmarks').done(function (data) {
            let benchmarks = data.results;
            search_page.update_benchmark_list(benchmarks, first_run);
        });
    }

    /**
     * Handle the list of all benchmarks from the server.
     * @param benchmarks The list of all benchmarks.
     * @param first_run True if this is on page load.
     */
    update_benchmark_list(benchmarks, first_run = false) {
        // clear out previous values
        let selection = document.getElementById("benchmark_selection");
        _clear_select(selection);

        let default_option = document.createElement('option');
        default_option.value = '';
        default_option.text = '';
        selection.add(default_option);

        for (const benchmark of benchmarks) {
            let option = document.createElement('option');
            option.value = benchmark['docker_name'];
            option.text = benchmark['docker_name'];
            selection.add(option);
        }

        if (first_run) {
            if (BENCHMARK_QUERY.length) {
                this.set_benchmark(BENCHMARK_QUERY);
            }
            this.search();
        }
    }

    /**
     * Display the column selection prompt.
     */
    make_column_select_prompt() {
        let activeColumns = document.getElementById("currentColumns");
        let availableColumns = document.getElementById("otherAvailableColumns");

        while (activeColumns.firstChild) {
            activeColumns.removeChild(activeColumns.firstChild);
        }

        const CORE_COLUMNS = [COLUMNS.CHECKBOX, COLUMNS.ACTIONS];

        for (let column of this.active_columns) {
            let columnOption = document.createElement("li");
            columnOption.classList.add("list-group-item", "list-group-item-action");
            if (column in COLUMNS) {
                if (CORE_COLUMNS.includes(COLUMNS[column])) {
                    columnOption.classList.add("core_column", "list-group-item-dark");
                }
                else {
                    columnOption.classList.add("list-group-item-secondary");
                }
                columnOption.textContent = COLUMNS[column];
            }
            else {
                if (this.notable_keys.includes(column)) {
                    columnOption.classList.add("list-group-item-primary");
                }
                columnOption.textContent = column;
            }
            columnOption.id = "column-select-" + column;
            activeColumns.appendChild(columnOption);
        }

        while (availableColumns.firstChild) {
            availableColumns.removeChild(availableColumns.firstChild);
        }
        let all_columns = _keys_from_object(COLUMNS).concat(this.notable_keys);
        for (let column of all_columns) {
            if (this.active_columns.includes(column)) {
                continue;
            }
            let columnOption = document.createElement("li");
            columnOption.classList.add("list-group-item");
            if (column in COLUMNS) {
                columnOption.classList.add("list-group-item-secondary");
                columnOption.textContent = COLUMNS[column];
            }
            else {
                columnOption.classList.add("list-group-item-primary");
                columnOption.textContent = column;
            }
            columnOption.textContent = COLUMNS[column];
            columnOption.id = "column-select-" + column;
            availableColumns.appendChild(columnOption);
        }

        this.activeSortable = new Sortable(activeColumns, {
            group: 'column_select',
            filter: '.core_column'
        });
        this.availableSortable = new Sortable(availableColumns, {
            group: 'column_select'
        });

        let modal = $('#columnSelectModal');
        modal.on('hidden.bs.modal', function e() {
            search_page.end_column_select_prompt();
        });
        modal.modal('show');
    }

    /**
     * Handle closing the column selection prompt and parse selection.
     */
    end_column_select_prompt() {
        let activeColumns = document.getElementById("currentColumns");

        let selected_columns = [];
        Array.from(activeColumns.children).forEach(function (option) {
            let value = option.id.slice("column-select-".length);
            selected_columns.push(value);
        });

        this.active_columns = selected_columns;
        this.update();

        delete this.activeSortable;
        delete this.availableSortable;
    }

    /**
     * Add adding a newly entered column name in #newColumnName
     */
    add_entered_column() {
        let availableColumns = document.getElementById("otherAvailableColumns");
        let newColumn = document.getElementById("newColumnName");
        if (!_validate_keypath(newColumn.value)) {
            newColumn.classList.add("is-invalid");
            if (document.getElementById("columnNameHelp") === null) {
                let helpDiv = document.createElement("div");
                helpDiv.id = "columnNameHelp";
                helpDiv.classList.add("invalid-feedback");
                helpDiv.textContent = "Please use correct syntax! (see JSON filter usage)";
                newColumn.parentElement.appendChild(helpDiv);
            }
            return;
        }
        else {
            let helpDiv = document.getElementById("columnNameHelp");
            if (helpDiv !== null) {
                helpDiv.parentElement.removeChild(helpDiv);
            }
            newColumn.classList.remove("is-invalid");
        }
        let newColumnOption = document.createElement("li");
        newColumnOption.classList.add("list-group-item");
        newColumnOption.textContent = newColumn.value;
        newColumnOption.id = "column-select-" + newColumn.value;
        availableColumns.appendChild(newColumnOption);
    }

    /**
     * Get the current diagram.
     * @returns {null} The current diagram, if any.
     */
    get_diagram() {
        return this.diagram;
    }

    /**
     * Get a list of the currently selected results.
     * @returns {*[]} The current selected results.
     */
    get_selected_results() {
        return this.results.filter(x => x[JSON_KEYS.get(FIELDS.CHECKBOX)]);
    }

    /**
     * Update diagram type selection.
     */
    select_diagram_type() {
        let diagram_chooser = document.getElementById("diagramDropdown");
        let configPanel = document.getElementById("diagramConfiguration-"
            + document.getElementById("diagramDropdown").value);
        if (configPanel !== undefined && configPanel !== null) {
            configPanel.classList.add("d-none");
        }
        switch (diagram_chooser.value) {
            case "speedup": {
                this.diagram = new SpeedupDiagram();
                this.diagram.updateData(this.get_selected_results());
                this.diagram.update_notable_keys(this.notable_keys);
                document.getElementById("diagramConfiguration-speedup").classList.remove("d-none");
            } break;
            default: {
                this._delete_diagram();
            } break;
        }
        if (this.diagram !== null) {
            this.diagram.updateData(this.get_selected_results());
        }
    }

    /**
     * Get the paginator.
      * @returns {PageNavigation} The active PageNavigation instance.
     */
    get_paginator() {
        return this.paginator;
    }

    update_diagram_configuration() {
        this.diagram.update_diagram_configuration();
    }

    /**
     * Delete the current diagram
     * @private
     */
    _delete_diagram() {
        if (this.diagram !== null && this.diagram !== undefined) {
            this.diagram.cleanup();
        }
        delete this.diagram;
        this.diagram = null;
    }

    /**
     * Allow the user to select a diagram when a benchmark is selected
     * @private
     */
    _enable_diagram_selection() {
        document.getElementById("diagramDropdown").disabled = false;
        document.getElementById("diagramDropdownBenchmarkHint").classList.add("d-none");
    }

    /**
     * Disable the diagram feature when no benchmark is selected
     * @private
     */
    _disable_diagram_selection() {
        document.getElementById("diagramDropdown").disabled = true;
        document.getElementById("diagramDropdownBenchmarkHint").classList.remove("d-none");
        document.getElementById("diagramDropdown").value = "";
        this._delete_diagram();
    }

    /**
     * Fetch notable keys for a given benchmark
     * @param benchmark_name the docker name of the benchmark
     * @private
     */
    _poll_notable_keys(benchmark_name) {
        $.ajax('/fetch_notable_benchmark_keys?query_json=' + encodeURI(JSON.stringify({docker_name: benchmark_name}))).done(function (data) {
            search_page.set_notable_keys(data['notable_keys']);
        });
    }
}

//
let search_page = null;

window.addEventListener("load", function () {
    search_page = new ResultSearch();
    search_page.onload();
});


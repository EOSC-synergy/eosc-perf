const FIELDS = {
    BENCHMARK: 'Benchmark',
    SITE: 'Site',
    UPLOADER: 'Uploader',
    DATA: 'Data',
    TAGS: 'Tags'
};

const COLUMNS = {
    CHECKBOX: 'Select',
    BENCHMARK: FIELDS.BENCHMARK,
    SITE: FIELDS.SITE,
    UPLOADER: FIELDS.UPLOADER,
    DATA: FIELDS.DATA,
    TAGS: FIELDS.TAGS,
    ACTIONS: 'Actions'
};

const FILTERS = {
    UPLOADER: FIELDS.UPLOADER,
    SITE: FIELDS.SITE,
    TAG: FIELDS.TAGS,
    JSON: "JSON-Key"
};

const FILTER_KEYS = new Map([
    [FILTERS.UPLOADER, "uploader"],
    [FILTERS.SITE, "site"],
    [FILTERS.TAG, "tag"],
    [FILTERS.JSON, "json"]
]);

const FILTER_HINTS = new Map([
    [FILTERS.UPLOADER, "user@example.com"],
    [FILTERS.SITE, "site short_name"],
    [FILTERS.TAG, "tag_name"],
    [FILTERS.JSON, "path.to.value"]
]);

const FILTER_HELPS = new Map([
    [FILTERS.UPLOADER, "The Uploader is described by the uploader's email. Different uploaders can be found in the table below in the <i>Uploader</i> column."],
    [FILTERS.SITE, "This field requires the site's short_name, which is a form of identifier. Sites can be found in the <i>Site</i> column in the result table below."],
    [FILTERS.TAG, "A tag is a short bit of text containing one or multiple keywords, such as <code>tensor</code> or <code>gpu_bound</code>."],
    [FILTERS.JSON, 'The search value has to describe the exact path within the JSON, separated with a dot.<br/>\
        <b>Example:</b><br/> \
        <code>{"example":{"nested":{"json":"value"},"different":{"path":{"to":"otherValue"}}}</code><br/> \
        <b>Correct:</b><br/> \
        example.nested.json or different.path.to \
        <b>Wrong:</b><br/> \
        json or example.nested or different:path:to']
]);

const FILTER_ID_PREFIX = {
    TYPE: "filter-type-",
    VALUE: "filter-value-",
    EXTRA_VALUE: "filter-extra-value-",
    SUGGESTIONS: "filter-suggestions-",
    COMPARISON: "filter-comparison-mode-",
    INFO: "filter-info-",
    EXTRA_FRAME: "filter-extra"
};

const JSON_MODES =  {
    LESS_THAN: 'lesser_than',
    EQUALS: 'equals',
    GREATER_THAN: 'greater_than'
};

const JSON_MODE_SYMBOLS = new Map([
    [JSON_MODES.LESS_THAN, '<'],
    [JSON_MODES.EQUALS, '='],
    [JSON_MODES.GREATER_THAN, '>']
]);

const JSON_KEYS = new Map([
    [COLUMNS.CHECKBOX, 'selected'],
    [COLUMNS.BENCHMARK, "benchmark"],
    [COLUMNS.SITE, "site"],
    [COLUMNS.UPLOADER, "uploader"],
    [COLUMNS.DATA, "data"],
    [COLUMNS.TAGS, "tags"]
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
function _format_nicely(item) {
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

class Table {
    /**
     * Construct a new table handler.
     */
    constructor() {
        this.table = document.getElementById("result_table");
    }

    /**
     * Remove all entries from the table.
     */
    _clear() {
        while (this.table.firstChild != null) {
            this.table.firstChild.remove();
        }
    }

    /**
     * Set up the top row of the table.
     */
    _create_head(columns) {
        let head = document.createElement("THEAD");
        for (const column of columns) {
            const column_name = (column in COLUMNS) ? COLUMNS[column] : _get_subkey_name(column);

            let cell = document.createElement("TH");

            if (!(column in COLUMNS)) {
                cell.setAttribute("data-toggle", "tooltip");
                cell.setAttribute("data-placement", "top");
                cell.setAttribute("title", column);
                if (column.includes(".")) {
                    cell.textContent = "(...)" + column_name;
                }
                else {
                    cell.textContent = column_name;
                }
            }
            else {
                cell.textContent = column_name;
            }
            cell.setAttribute("scope", "col");

            switch (column_name) {
                case (COLUMNS.CHECKBOX): {
                    // sort by selected results
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => x["selected"] < y["selected"], column_name);
                    });
                }
                    break;
                case (COLUMNS.BENCHMARK): {
                    // alphabetically sort by benchmark
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => x["benchmark"] < y["benchmark"], column_name);
                    });
                }
                    break;
                case (COLUMNS.SITE): {
                    // alphabetically sort by site
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => x["site"] < y["site"], column_name);
                    });
                }
                    break;
                case (COLUMNS.UPLOADER): {
                    // alphabetically sort by uploader
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => x["uploader"] < y["uploader"], column_name);
                    });
                }
                    break;
                case (COLUMNS.DATA):
                    // Not clear what to sort after.
                    break;
                case (COLUMNS.TAGS):
                    // todo find order on tags
                    break;
                default:
                    cell.addEventListener("click", function() {
                        // TODO: sorting helpers
                        search_page.sort_by( (x, y) => _fetch_subkey(x["data"], column) < _fetch_subkey(y["data"], column), column);
                    });
                    break;
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

            for (const key of columns) {
                const column = (key in COLUMNS) ? COLUMNS[key] : key;
                let cell = document.createElement("TD");
                switch (column) {
                    case (COLUMNS.CHECKBOX): {
                        let select = document.createElement("input");
                        select.setAttribute("type", "checkbox");
                        select.setAttribute("id", "selected" + i);
                        if (result[JSON_KEYS.get(column)]) {
                            select.setAttribute("checked", "");
                        }
                        select.setAttribute('style', 'height: 1.5em');
                        // when clicked, select
                        select.addEventListener("click", function () {
                            search_page.select_result(i + startIndex);
                        });
                        cell.appendChild(select);
                    } break;

                    case (COLUMNS.DATA): {
                        let view_button = document.createElement("input");
                        view_button.setAttribute("type", "submit");
                        view_button.setAttribute("value", "View JSON");
                        view_button.setAttribute("class", "btn btn-secondary btn-sm");
                        view_button.addEventListener("click", function () {
                            search_page.display_json(JSON.stringify(result[JSON_KEYS.get(column)], null, 4));
                        });

                        // set hover-text to content
                        //view_data.setAttribute("title", JSON.stringify(result[column], null, "\t"));
                        cell.appendChild(view_button);
                    } break;

                    case (COLUMNS.UPLOADER): {
                        let mailLink = document.createElement("a");
                        mailLink.href = "mailto:" + result[JSON_KEYS.get(column)];
                        mailLink.setAttribute("data-toggle", "tooltip");
                        mailLink.setAttribute("data-placement", "top");
                        mailLink.setAttribute("title", result[JSON_KEYS.get(column)]);
                        mailLink.textContent = "Contact";
                        cell.appendChild(mailLink);
                    } break;

                    case (COLUMNS.SITE):
                    case (COLUMNS.TAGS):
                    case (COLUMNS.BENCHMARK): {
                        cell.textContent = result[JSON_KEYS.get(column)];
                    } break;

                    case COLUMNS.ACTIONS: {
                        // actions
                        let div = document.createElement('div');
                        div.classList.add('btn-group');

                        let actions_report = document.createElement("button");
                        actions_report.textContent = 'Report';
                        actions_report.classList.add('btn', 'btn-warning', 'btn-sm');
                        actions_report.setAttribute('type', 'button');
                        actions_report.addEventListener('click', function () {
                            search_page.report_result(result);
                        });
                        div.appendChild(actions_report);

                        if (admin) {
                            let actions_delete = document.createElement('button');
                            actions_delete.textContent = 'Delete';
                            actions_delete.classList.add('btn', 'btn-danger', 'btn-sm');
                            actions_delete.setAttribute('type', 'button');
                            actions_delete.addEventListener('click', function () {
                                search_page.delete_result(result);
                            });
                            div.appendChild(actions_delete);
                        }
                        cell.appendChild(div);
                        row.appendChild(cell);
                    } break;

                    default: {
                        cell.textContent = _format_nicely(_fetch_subkey(result["data"], column));
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
}

class PageNavigation {
    /**
     * Set up page navigation handler.
     */
    constructor() {
        this.current_page = 0;
        this.results_per_page = 10;
        this.page_count = 1;
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
     * Update the current number of results.
     * @param result_count The new number of results.
     */
    set_result_count(result_count) {
        this.page_count = Math.max(Math.ceil(result_count / this.results_per_page), 1);
        if (this.current_page >= this.page_count) {
            this.current_page = this.page_count - 1;
        }
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
        /** Reads the selected results per page and updates teh site accordingly. */
        this.results_per_page = document.getElementById("results_on_page").value;
        // Restart at page 1;
        this.current_page = 0;
        this.update();
        search_page.update();
    }
}

class Diagram {
    update_notable_keys(notable_keys) {
    }
    update(results) {
    }
    cleanup() {
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

        let section = document.getElementById("diagramSection");
        {
            let xAxisDiv = document.createElement("div");
            xAxisDiv.classList.add("form-inline");
            {
                let label = document.createElement("label");
                label.setAttribute("for", "diagramX");
                label.textContent = "X Axis:";
                xAxisDiv.appendChild(label);

                let dropdown = document.createElement("select");
                dropdown.setAttribute("id", "diagramX");
                dropdown.classList.add("form-control");
                dropdown.onchange = function() {
                    search_page.get_diagram().refresh();
                };
                xAxisDiv.appendChild(dropdown);
            }
            section.appendChild(xAxisDiv);

            let yAxisDiv = document.createElement("div");
            yAxisDiv.classList.add("form-inline");
            {
                let label = document.createElement("label");
                label.setAttribute("for", "diagramY");
                label.textContent = "Y Axis:";
                yAxisDiv.appendChild(label);

                let dropdown = document.createElement("select");
                dropdown.setAttribute("id", "diagramY");
                dropdown.classList.add("form-control");
                dropdown.onchange = function() {
                    search_page.get_diagram().refresh();
                };
                yAxisDiv.appendChild(dropdown);
            }
            section.appendChild(yAxisDiv);

            let canvas = document.createElement("canvas");
            canvas.setAttribute("id", "speedup");
            section.appendChild(canvas);

            let interactions = document.createElement("div");
            {
                let downloadButton = document.createElement("button");
                downloadButton.setAttribute("id", "downloadButton");
                downloadButton.setAttribute("type", "button");
                downloadButton.classList.add("btn", "btn-light");
                downloadButton.textContent = "Download as PNG";
                downloadButton.onclick = function() {
                    search_page.get_diagram().downloadPNG();
                };
                interactions.appendChild(downloadButton);

                let csvButton = document.createElement("button");
                csvButton.setAttribute("id", "csvButton");
                csvButton.setAttribute("type", "button");
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
     * Build a chart.js dataset off current data
     *
     * TODO: add nulls for columns this dataset has no value for
     *
     * @returns {{spanGaps: boolean, backgroundColor: (string|*), borderColor: (string|string), data: [], borderWidth: number, label: (*|string)}} Chart.js dataset
     * @private
     */
    _buildDataset() {
        let color = Chart.helpers.color;
        let scores = [];
        for (const value of this.results) {
            scores.push(_fetch_subkey(value.data, this.yAxis));
        }
        return {
            label: _get_subkey_name(this.yAxis),
            backgroundColor: color(CHART_COLORS[0]).alpha(0.5).rgbString(),
            borderColor: CHART_COLORS[0],
            borderWidth: 1,
            data: scores,
            spanGaps: true
        };
    }

    /**
     * Build an array of chart column labels off current data
     * @returns {[]} An array of labels.
     * @private
     */
    _buildLabels() {
        let labels = [];
        let sameSite = true;
        if (this.results.length !== 0) {
            let siteName = _fetch_subkey(this.results[0].data, JSON_KEYS.get(COLUMNS.SITE));
            for (const result of this.results) {
                sameSite &&= (_fetch_subkey(result.data, JSON_KEYS.get(COLUMNS.SITE)) === siteName);
                if (sameSite === false) {
                    break;
                }
            }
        }
        else {
            sameSite = false;
        }
        for (const value of this.results) {
            let label = _fetch_subkey(value.data, this.xAxis);
            if (sameSite) {
                labels.push(label.toString());
            }
            else {
                labels.push(_fetch_subkey(value, JSON_KEYS.get(COLUMNS.SITE)) + ', ' + label.toString());
            }
        }
        return labels;
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

        let xAxisSelect = document.getElementById("diagramX");
        _clear_select(xAxisSelect);
        let yAxisSelect = document.getElementById("diagramY");
        _clear_select(yAxisSelect);
        for (const key of notable_keys) {
            let xOption = document.createElement("option");
            xOption.setAttribute("value", key);
            xOption.textContent = key;
            xAxisSelect.appendChild(xOption);

            let yOption = document.createElement("option");
            yOption.setAttribute("value", key);
            yOption.textContent = key;
            yAxisSelect.appendChild(yOption);
        }
    }

    /**
     * Update diagram chart
     */
    refresh() {
        if (window.diagram !== null && window.diagram !== undefined) {
            window.diagram.destroy();
            delete window.diagram;
        }
        this.xAxis = document.getElementById("diagramX").value;
        this.yAxis = document.getElementById("diagramY").value;
        if (!_validate_keypath(this.xAxis) || !_validate_keypath(this.yAxis) || this.results.length === 0) {
            document.getElementById("downloadButton").setAttribute("disabled", "true");
            document.getElementById("csvButton").setAttribute("disabled", "true");
            document.getElementById("speedup").style.display = "none";
            return;
        }
        else {
            document.getElementById("speedup").style.removeProperty("display");
        }

        let dataSets = [this._buildDataset()];
        let labels = this._buildLabels();

        let context = document.getElementById('speedup').getContext('2d');
        window.diagram = new Chart(context, {
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
                    text: 'SpeedupDiagram'
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
                }
            }
        });

        document.getElementById("downloadButton").removeAttribute("disabled");
        document.getElementById("csvButton").removeAttribute("disabled");
    }

    /**
     * Update diagram data
     * @param data The new results to use.
     */
    update(data) {
        this.results = data;

        this.refresh();
    }

    /**
     * Remove data associated to this component, such as chart.js objects and HTML elements.
     */
    cleanup() {
        if (window.diagram) {
            window.diagram.destroy();
        }

        // naïve purge
        _clear_select(document.getElementById("diagramSection"));
    }
}

/**
 * The ResultSearch class is responsible to communicate with the backend to get the search results and display them.
 * TODO: split into smaller parts
 */
class ResultSearch extends Content {
    /**
     * Set up result search.
     */
    constructor() {
        super();

        this.results = [];
        this.filters = [];
        this.ordered_by = null;
        this.current_filter_id = 0;
        this.filter_ids = [];
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
        this.search();
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
            this.diagram.update(this.get_selected_results());
        }

        $('[data-toggle="popover"]').popover({
            html: true
        });

        $('[data-toggle="tooltip"]').tooltip();
    }

    /**
     * Display the specified JSON in a popup.
     * @param json The JSON data to display.
     */
    display_json(json) {
        document.getElementById('jsonPreviewContent').textContent = json;
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

        for (let filter_id of this.filter_ids) {
            let filter = {};
            let filter_type = document.getElementById(FILTER_ID_PREFIX.TYPE + filter_id).value;
            let filter_value = document.getElementById(FILTER_ID_PREFIX.VALUE + filter_id).value;
            let filter_compare = document.getElementById(FILTER_ID_PREFIX.COMPARISON + filter_id).value;
            let filter_extra_value = document.getElementById(FILTER_ID_PREFIX.EXTRA_VALUE + filter_id).value;
            filter['type'] = FILTER_KEYS.get(filter_type);
            if (filter_type.toString().localeCompare(FILTERS.JSON) === 0) {
                filter['value'] = filter_extra_value;
                filter['key'] = filter_value;
                filter['mode'] = filter_compare;
                if (filter_value && filter_extra_value) {
                    filters.push(filter);
                }
            }
            else {
                filter['value'] = filter_value;
                if (filter_value) {
                    filters.push(filter);
                }
            }
        }

        // Finish query.
        let query = { "filters": filters };

        document.getElementById('loading-icon').classList.add('loading');

        // Find get new results via ajax query.
        $.ajax('/query_results?query_json=' + encodeURI(JSON.stringify(query)))
            .done(function (data) {
                search_page.results = data["results"];
                if (search_page.results.length > 0) {
                    // add selected col
                   search_page.results.forEach(element => {
                        element[JSON_KEYS.get(COLUMNS.CHECKBOX)] = false;
                    });
                }
                search_page.current_page = 1;
                search_page.get_paginator().set_result_count(search_page.get_result_count());
                search_page.update();
                document.getElementById('loading-icon').classList.remove('loading');
            });
        return false;
    }

    /**
     * Add a filter field consisting of a selection of filter type, one or two input fields and the option of removing
     * the created filter field.
     * @param input_values An optional object witch should contain a subset of following attributes filter_type (the
     *                     type of filter, the value should be element of filter_types), input (input value of
     *                     corresponding filter), num_input (numeric input value of corresponding filter).
     */
    add_filter_field(input_values) {
        let filter_id = "f" + this.current_filter_id++;

        let filter_list = document.getElementById('filters');

        // add line for the filter
        let new_filter = document.createElement('LI');
        new_filter.setAttribute("id", filter_id);
        //new_filter.setAttribute("class", "flexbox filter");
        new_filter.classList.add("form-inline");

        // Remove this filter
        let remove_filter = document.createElement("button");
        remove_filter.setAttribute("type", "button");
        remove_filter.classList.add("close");
        remove_filter.setAttribute("aria-label", "Close");
        // label
        {
            let remove_filter_label = document.createElement("span");
            remove_filter_label.setAttribute("aria-hidden", "true");
            remove_filter_label.textContent = "×";
            remove_filter.appendChild(remove_filter_label);
        }
        remove_filter.addEventListener("click", function () {
            search_page.remove_filter(filter_id);
        });
        new_filter.appendChild(remove_filter);

        // filter type selection
        let filter_type = document.createElement("select");
        filter_type.setAttribute("id", FILTER_ID_PREFIX.TYPE + filter_id);
        for (let filter in FILTERS) {
            let type = document.createElement("OPTION");
            type.setAttribute("value", FILTERS[filter]);
            type.textContent = FILTERS[filter];
            filter_type.appendChild(type);
        }
        new_filter.appendChild(filter_type);

        // On change callback
        filter_type.addEventListener("change", function () {
            document.getElementById(FILTER_ID_PREFIX.VALUE + filter_id).placeholder = FILTER_HINTS.get(filter_type.value);
            document.getElementById(FILTER_ID_PREFIX.INFO + filter_id)
                .setAttribute("data-content", FILTER_HELPS.get(filter_type.value));

            // hide extra json input on other filters
            document.getElementById(FILTER_ID_PREFIX.EXTRA_FRAME + filter_id).style.visibility = "hidden";
            if (filter_type.value.localeCompare(FILTERS.JSON) === 0) {
                document.getElementById(FILTER_ID_PREFIX.EXTRA_FRAME + filter_id).style.visibility = "visible";
            }
        });
        filter_type.classList.add("form-control");

        // Primary input
        let input_div = document.createElement("div");
        input_div.classList.add("input-group");
        // textbox
        {
            let input = document.createElement("input");
            input.setAttribute("type", "text");
            input.setAttribute("id", FILTER_ID_PREFIX.VALUE + filter_id);
            input.setAttribute("placeholder", "Filter Value");
            input.classList.add("form-control");
            input_div.appendChild(input);
        }
        // suggestions menu
        {
            let input_extras = document.createElement("div");
            input_extras.classList.add("input-group-append");
            {
                let suggestions_button = document.createElement("button");
                suggestions_button.classList.add("btn", "btn-outline-secondary", "dropdown-toggle", "dropdown-toggle-split");
                suggestions_button.setAttribute("data-toggle", "dropdown");
                suggestions_button.setAttribute("aria-haspopup", "true");
                suggestions_button.setAttribute("aria-expanded", "false");
                suggestions_button.setAttribute("type", "button");

                {
                    let suggestions_button_screenreader_hint = document.createElement("span");
                    suggestions_button_screenreader_hint.classList.add("sr-only");
                    suggestions_button_screenreader_hint.textContent = "Toggle Dropdown";
                    suggestions_button.appendChild(suggestions_button_screenreader_hint);
                }
                input_extras.appendChild(suggestions_button);
            }

            // Info button
            {
                let type_info = document.createElement("input");
                type_info.setAttribute("type", "button");
                type_info.setAttribute("id", FILTER_ID_PREFIX.INFO + filter_id);
                type_info.setAttribute("class", "btn", "btn-outline-warning");
                type_info.setAttribute("value", "?");
                type_info.setAttribute("data-toggle", "popover");
                type_info.setAttribute("title", "Format Description");
                type_info.setAttribute("data-content", "You find some Tips for the expected input values here.");
                type_info.setAttribute("data-placement", "right");
                input_extras.appendChild(type_info);
            }

            // Suggestions
            {
                let suggestions = document.createElement("div");
                suggestions.classList.add("dropdown-menu");
                suggestions.setAttribute("id", FILTER_ID_PREFIX.SUGGESTIONS + filter_id);
                if (this.notable_keys.length === 0) {
                    let suggestion_option = document.createElement("a");
                    suggestion_option.classList.add("dropdown-item");
                    suggestion_option.textContent = "No suggestions found!";
                    suggestions.append(suggestion_option);
                }
                else {
                    for (let notable of this.notable_keys) {
                        let suggestion_option = document.createElement("a");
                        suggestion_option.classList.add("dropdown-item");
                        suggestion_option.textContent = notable;
                        suggestion_option.addEventListener("click", function (event) {
                            document.getElementById(FILTER_ID_PREFIX.VALUE + filter_id).value = suggestions.value;
                            document.getElementById(FILTER_ID_PREFIX.VALUE + filter_id).textContent = suggestions.value;
                        });
                        suggestions.append(suggestion_option);
                    }
                }
                input_extras.appendChild(suggestions);
            }

            input_div.appendChild(input_extras);
        }
        new_filter.appendChild(input_div);

        // Extra JSON input
        let extra_input_field = document.createElement("div");
        extra_input_field.classList.add("input-group");
        extra_input_field.setAttribute("id", FILTER_ID_PREFIX.EXTRA_FRAME + filter_id);
        extra_input_field.style.visibility = "hidden";
        // comparison mode dropdown
        {
            let json_mode_prepend = document.createElement("div");
            json_mode_prepend.classList.add("input-group-prepend");
            {
                let json_mode = document.createElement("button");
                json_mode.classList.add("btn", "btn-outline-secondary", "dropdown-toggle");
                json_mode.setAttribute("id", FILTER_ID_PREFIX.COMPARISON + filter_id);
                json_mode.setAttribute("type", "button");
                json_mode.setAttribute("data-toggle", "dropdown");
                json_mode.setAttribute("aria-haspopup", "true");
                json_mode.setAttribute("aria-expanded", "false");
                json_mode.value = JSON_MODES.GREATER_THAN;
                json_mode.textContent = JSON_MODE_SYMBOLS.get(JSON_MODES.GREATER_THAN);
                json_mode_prepend.appendChild(json_mode);

                let json_mode_dropdown = document.createElement("div");
                json_mode_dropdown.classList.add("dropdown-menu");
                for (let mode in JSON_MODES) {
                    mode = JSON_MODES[mode];
                    let mode_option = document.createElement("a");
                    mode_option.classList.add("dropdown-item");
                    mode_option.value = mode;
                    mode_option.textContent = JSON_MODE_SYMBOLS.get(mode);
                    mode_option.addEventListener("click", function() {
                        json_mode.value = mode;
                        json_mode.textContent = JSON_MODE_SYMBOLS.get(mode);
                    });
                    json_mode_dropdown.appendChild(mode_option);
                }
                json_mode_prepend.appendChild(json_mode_dropdown);
            }
            extra_input_field.appendChild(json_mode_prepend);
        }
        // json value input
        {
            let num_input = document.createElement("input");
            num_input.setAttribute("id", FILTER_ID_PREFIX.EXTRA_VALUE + filter_id);
            num_input.setAttribute("min", "0");
            num_input.classList.add("form-control");
            extra_input_field.appendChild(num_input);
        }
        new_filter.appendChild(extra_input_field);

        filter_list.appendChild(new_filter);

        this.filter_ids.push(filter_id);

        // Activate popover.
        $('[data-toggle="popover"]').popover({
            html: true
        });
    }

    /**
     * Remove a filter field by id.
     * @param filter_id The id of the filter field to remove.
     */
    remove_filter(filter_id) {
        /** Remove the filter*/
        document.getElementById(filter_id).remove();
        this.filter_ids.filter(function(value, index, arr) {
            return value.localeCompare(filter_id) !== 0;
        });
    }

    /**
     * Sort the results by a given column.
     * @param callback A function taking tow results and returning a bool, in  a way a order is defined.
     * @param column Which column to sort by.
     */
    sort_by(callback, column) {
        this.results.sort(callback);
        // reverse order if double clicked.
        if (this.ordered_by === column) {
            this.results = this.results.reverse();
            this.ordered_by = "";
        } else {
            this.ordered_by = column;
        }
        this.update();
        // remove possible column hover tooltips
        $('.tooltip').remove();
    }

    /**
     * Select a specific result.
     * @param result_number The index of the result to select.
     */
    select_result(result_number) {
        this.results[result_number][JSON_KEYS.get(COLUMNS.CHECKBOX)] ^= true;
        this.diagram.update(this.get_selected_results());
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
            alert(data);
            if (data.toLowerCase.includes("success")) {
                this.results.filter(function (r) {
                    return r["uuid"] === result;
                });
                search_page.update();
            }
        });
        return false;
    }

    /**
     * Invert the current result selection
     * @returns {boolean} false (skip other event listener)
     */
    invert_selection() {
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
            $.ajax('/fetch_notable_benchmark_keys?query_json=' + encodeURI(JSON.stringify({docker_name: benchmark_name})))
            .done(function (data) {
                search_page.set_notable_keys(data['notable_keys']);
            });
        }
        else {
            this.set_notable_keys([]);
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
     * Update all notable-JSON-field suggestion dropdowns
     * @private
     */
    _update_json_suggestions() {
        for (let filter of this.filter_ids) {
            let div = document.getElementById(FILTER_ID_PREFIX.SUGGESTIONS + filter);
            while (div.firstChild) {
                div.removeChild(div.firstChild);
            }
            if (this.notable_keys.length === 0) {
                let suggestion_option = document.createElement("a");
                suggestion_option.classList.add("dropdown-item");
                suggestion_option.textContent = "No suggestions found!";
                div.append(suggestion_option);
            }
            else {
                for (let notable of this.notable_keys) {
                    let suggestion_option = document.createElement("a");
                    suggestion_option.classList.add("dropdown-item");
                    suggestion_option.textContent = notable;
                    suggestion_option.addEventListener("click", function (event) {
                        document.getElementById(FILTER_ID_PREFIX.VALUE + filter).value = notable;
                        document.getElementById(FILTER_ID_PREFIX.VALUE + filter).textContent = notable;
                    });
                    div.appendChild(suggestion_option);
                }
            }
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

        this._update_json_suggestions();

        if (this.diagram !== null) {
            this.diagram.update_notable_keys(this.notable_keys);
        }
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
        while (selection.options.length > 0) {
            selection.remove(0);
        }

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
        for (let column of this.active_columns) {
            let columnOption = document.createElement("li");
            columnOption.classList.add("list-group-item", "list-group-item-action");
            if (column in COLUMNS) {
                columnOption.classList.add("core_column", "list-group-item-secondary");
            }
            columnOption.textContent = column;
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
            columnOption.textContent = column;
            availableColumns.appendChild(columnOption);
        }

        this.activeSortable = new Sortable(activeColumns, {
            group: 'column_select',
            filter: '.core_column'
        });
        this.availableSortable = new Sortable(availableColumns, {
            group: 'column_select'
        });

        $('#columnSelectModal').on('hidden.bs.modal', function e() {
            search_page.end_column_select_prompt();
        });
        $('#columnSelectModal').modal('show');
    }

    /**
     * Handle closing the column selection prompt and parse selection.
     */
    end_column_select_prompt() {
        let activeColumns = document.getElementById("currentColumns");

        let selected_columns = [];
        Array.from(activeColumns.children).forEach(function (option) {
            selected_columns.push(option.textContent);
        });

        this.active_columns = selected_columns;
        this.update();
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
                helpDiv.setAttribute("id", "columnNameHelp");
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
        return this.results.filter(x => x[JSON_KEYS.get(COLUMNS.CHECKBOX)]);
    }

    /**
     * Update diagram type selection.
     */
    select_diagram_type() {
        let diagram_chooser = document.getElementById("diagramDropdown");
        switch (diagram_chooser.value) {
            case "speedup": {
                this.diagram = new SpeedupDiagram();
                this.diagram.update(this.get_selected_results());
                this.diagram.update_notable_keys(this.notable_keys);
            } break;
            default: {
                if (this.diagram !== null && this.diagram !== undefined) {
                    this.diagram.cleanup();
                }
                delete this.diagram;
                this.diagram = null;
            } break;
        }
    }

    /**
     * Get the paginator.
      * @returns {PageNavigation} The active PageNavigation instance.
     */
    get_paginator() {
        return this.paginator;
    }
}

//
let search_page = null;

window.addEventListener("load", function () {
    search_page = new ResultSearch();
    search_page.onload();
});


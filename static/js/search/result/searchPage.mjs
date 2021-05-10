import { PageNavigation } from './navigation.mjs';
import { Table } from './resultTable.mjs';
import { Filter } from './filter.mjs';
import { SpeedupDiagram } from './diagram.mjs';
import { clear_select, FIELDS, JSON_KEYS, validate_keypath } from './helpers.mjs';

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
 * The ResultSearch class is responsible to communicate with the backend to get the search results and display them.
 * TODO: split into smaller parts
 */
export class ResultSearch {
    /**
     * Set up result search.
     */
    constructor() {
        this.results = [];
        this.filters = [];
        this.ordered_by = null;
        this.filters = [];
        this.notable_keys = [];

        this.active_columns = [];
        this._populate_active_columns();

        this.table = new Table();
        this.paginator = new PageNavigation();

        this.benchmark_name = '';

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
            html: true,
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
            html: true,
        });

        $('[data-toggle="tooltip"]').tooltip();
    }

    /**
     * Display the specified result in a popup.
     * @param result The result to display.
     */
    display_result(result) {
        document.getElementById('jsonPreviewContent').textContent = JSON.stringify(
            result.data,
            null,
            4
        );
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
                type: 'benchmark',
                value: this.benchmark_name,
            });
        }

        for (let filter of this.filters) {
            let filterInfo = {};
            const filterType = filter.getType();
            const value = filter.getValue();

            filterInfo['type'] = Filter.KEYS.get(filterType);
            if (filterType.toString().localeCompare(Filter.TYPES.JSON) === 0) {
                const jsonValue = filter.getJsonValue();
                filterInfo['value'] = jsonValue;
                filterInfo['key'] = filter.getValue();
                filterInfo['mode'] = filter.getJsonMode();
                if (value && jsonValue) {
                    filters.push(filterInfo);
                }
            } else {
                filterInfo['value'] = value;
                if (value) {
                    filters.push(filterInfo);
                }
            }
        }

        // Finish query.
        let query = { filters: filters };

        document.getElementById('loading-icon').classList.add('loading');

        // Find get new results via ajax query.
        $.ajax('/ajax/query/results?query_json=' + encodeURI(JSON.stringify(query)))
            .fail(function (jqXHR, textStatus, errorThrown) {
                if (jqXHR.status === 401) {
                    // unauthorized query (uploader)
                    // TODO: how should we display error messages inline? popup? toast?
                }
                search_page.results = [];
                console.error('Error', jqXHR.status, 'occured while searching searching');
            })
            .done(function (data) {
                if (!data.hasOwnProperty('results')) {
                    console.error('Search page returned no data!');
                    return;
                }
                search_page.results = data['results'];
                if (search_page.results.length > 0) {
                    // add selected col
                    search_page.results.forEach((element) => {
                        element[JSON_KEYS.get(FIELDS.CHECKBOX)] = false;
                    });
                }
            })
            .always(function () {
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
        } else {
            console.error('Failed to remove filter from internal filter list!');
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
            this.table.set_column_sort(column, Table.SORT_ORDER.REVERSED);
        } else {
            this.results.sort(callback);
            this.table.set_column_sort(column, Table.SORT_ORDER.NORMAL);
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
        this.open_new_tab('/report/result' + '?uuid=' + result['uuid']);
    }

    /**
     * Delete a given result.
     * @param result The result to delete.
     * @returns {boolean} false (skip other event listener)
     */
    delete_result(result) {
        submit_json(
            '/ajax/delete/result',
            { uuid: result['uuid'] },
            function (data, textStatus) {
                search_page.table.mark_result_as_removed(result.uuid);
                search_page.results = search_page.results.filter(function (r) {
                    return r.uuid !== result.uuid;
                });
            },
            function (data) {
                display_message('Could not remove result!');
            }
        );
        return false;
    }

    /**
     * Invert the current result selection
     * @returns {boolean} false (skip other event listener)
     */
    selection_invert() {
        if (this.results.length === 0) {
            return false;
        }
        this.results.forEach((r) => {
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
        if (this.results.length === 0) {
            return false;
        }
        this.results.forEach((r) => {
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
        let selection = document.getElementById('benchmark_selection');
        for (let i = 0; i < selection.options.length; i++) {
            if (selection.options[i].value.localeCompare(benchmark_name) === 0) {
                selection.selectedIndex = i;
            }
        }

        if (benchmark_name.length > 0) {
            this._poll_notable_keys(benchmark_name);

            let infoButton = document.getElementById('dockerhubLinkButton');
            infoButton.onclick = function () {
                open_tab('https://hub.docker.com/r/' + benchmark_name.split(':')[0]);
            };
            infoButton.disabled = false;

            this._enable_diagram_selection();
        } else {
            this.set_notable_keys([]);
            document.getElementById('dockerhubLinkButton').disabled = true;

            this._disable_diagram_selection();
        }
    }

    /**
     * Callback for benchmark selection dropdown.
     */
    update_benchmark_selection() {
        let selected_benchmark = document.getElementById('benchmark_selection').value;
        this.set_benchmark(selected_benchmark);
        this.search();
    }

    /**
     * Fill active column list with all default columns and notable keys
     * @private
     */
    _populate_active_columns() {
        for (let column in Table.DEFAULT_COLUMNS) {
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
        $.ajax('/ajax/fetch/benchmarks').done(function (data) {
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
        let selection = document.getElementById('benchmark_selection');
        clear_select(selection);

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
            this.set_benchmark(BENCHMARK_QUERY);
            this.search();
        }
    }

    /**
     * Display the column selection prompt.
     *
     * TODO: make this an object
     */
    make_column_select_prompt() {
        let activeColumns = document.getElementById('currentColumns');
        let availableColumns = document.getElementById('otherAvailableColumns');

        while (activeColumns.firstChild) {
            activeColumns.removeChild(activeColumns.firstChild);
        }

        const CORE_COLUMNS = [Table.DEFAULT_COLUMNS.CHECKBOX, Table.DEFAULT_COLUMNS.ACTIONS];

        for (let column of this.active_columns) {
            let columnOption = document.createElement('li');
            columnOption.classList.add('list-group-item', 'list-group-item-action');
            if (column in Table.DEFAULT_COLUMNS) {
                if (CORE_COLUMNS.includes(Table.DEFAULT_COLUMNS[column])) {
                    columnOption.classList.add('core_column', 'list-group-item-dark');
                } else {
                    columnOption.classList.add('list-group-item-secondary');
                }
                columnOption.textContent = Table.DEFAULT_COLUMNS[column];
            } else {
                if (this.notable_keys.includes(column)) {
                    columnOption.classList.add('list-group-item-primary');
                }
                columnOption.textContent = column;
            }
            columnOption.id = 'column-select-' + column;
            activeColumns.appendChild(columnOption);
        }

        while (availableColumns.firstChild) {
            availableColumns.removeChild(availableColumns.firstChild);
        }
        let all_columns = _keys_from_object(Table.DEFAULT_COLUMNS).concat(this.notable_keys);
        for (let column of all_columns) {
            if (this.active_columns.includes(column)) {
                continue;
            }
            let columnOption = document.createElement('li');
            columnOption.classList.add('list-group-item');
            if (column in Table.DEFAULT_COLUMNS) {
                columnOption.classList.add('list-group-item-secondary');
                columnOption.textContent = Table.DEFAULT_COLUMNS[column];
            } else {
                columnOption.classList.add('list-group-item-primary');
                columnOption.textContent = column;
            }
            columnOption.textContent = Table.DEFAULT_COLUMNS[column];
            columnOption.id = 'column-select-' + column;
            availableColumns.appendChild(columnOption);
        }

        this.activeSortable = new Sortable(activeColumns, {
            group: 'column_select',
            filter: '.core_column',
        });
        this.availableSortable = new Sortable(availableColumns, {
            group: 'column_select',
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
        let activeColumns = document.getElementById('currentColumns');

        let selected_columns = [];
        Array.from(activeColumns.children).forEach(function (option) {
            let value = option.id.slice('column-select-'.length);
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
        let availableColumns = document.getElementById('otherAvailableColumns');
        let newColumn = document.getElementById('newColumnName');
        if (!validate_keypath(newColumn.value)) {
            newColumn.classList.add('is-invalid');
            if (document.getElementById('columnNameHelp') === null) {
                let helpDiv = document.createElement('div');
                helpDiv.id = 'columnNameHelp';
                helpDiv.classList.add('invalid-feedback');
                helpDiv.textContent = 'Please use correct syntax! (see JSON filter usage)';
                newColumn.parentElement.appendChild(helpDiv);
            }
            return;
        } else {
            let helpDiv = document.getElementById('columnNameHelp');
            if (helpDiv !== null) {
                helpDiv.parentElement.removeChild(helpDiv);
            }
            newColumn.classList.remove('is-invalid');
        }
        let newColumnOption = document.createElement('li');
        newColumnOption.classList.add('list-group-item');
        newColumnOption.textContent = newColumn.value;
        newColumnOption.id = 'column-select-' + newColumn.value;
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
        return this.results.filter((x) => x[JSON_KEYS.get(FIELDS.CHECKBOX)]);
    }

    /**
     * Update diagram type selection.
     */
    select_diagram_type() {
        let diagram_chooser = document.getElementById('diagramDropdown');
        let configPanel = document.getElementById(
            'diagramConfiguration-' + document.getElementById('diagramDropdown').value
        );
        if (configPanel !== undefined && configPanel !== null) {
            configPanel.classList.add('d-none');
        }
        switch (diagram_chooser.value) {
            case 'speedup':
                {
                    this.diagram = new SpeedupDiagram();
                    this.diagram.updateData(this.get_selected_results());
                    this.diagram.update_notable_keys(this.notable_keys);
                    document
                        .getElementById('diagramConfiguration-speedup')
                        .classList.remove('d-none');
                }
                break;
            default:
                {
                    this._delete_diagram();
                }
                break;
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
        document.getElementById('diagramDropdown').disabled = false;
        document.getElementById('diagramDropdownBenchmarkHint').classList.add('d-none');
    }

    /**
     * Disable the diagram feature when no benchmark is selected
     * @private
     */
    _disable_diagram_selection() {
        document.getElementById('diagramDropdown').disabled = true;
        document.getElementById('diagramDropdownBenchmarkHint').classList.remove('d-none');
        document.getElementById('diagramDropdown').value = '';
        this._delete_diagram();
    }

    /**
     * Fetch notable keys for a given benchmark
     * @param benchmark_name the docker name of the benchmark
     * @private
     */
    _poll_notable_keys(benchmark_name) {
        $.ajax(
            '/ajax/fetch/notable_benchmark_keys?query_json=' +
                encodeURI(JSON.stringify({ docker_name: benchmark_name }))
        ).done(function (data) {
            search_page.set_notable_keys(data['notable_keys']);
        });
    }
}

// singleton
export let search_page = null;

export function init_search_page() {
    search_page = new ResultSearch();
}

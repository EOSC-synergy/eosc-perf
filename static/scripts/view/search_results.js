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
    BENCHMARK: FIELDS.BENCHMARK,
    UPLOADER: FIELDS.UPLOADER,
    SITE: FIELDS.SITE,
    TAG: FIELDS.TAGS,
    JSON_GREATER_THAN: "Value greater than",
    JSON_EQUAL: "Value equal to",
    JSON_LESS_THAN: "Value less than"
};

const FILTER_KEYS = new Map([
    [FILTERS.BENCHMARK, 'benchmark'],
    [FILTERS.UPLOADER, 'uploader'],
    [FILTERS.SITE, 'site'],
    [FILTERS.TAG, 'tag'],
    [FILTERS.JSON_GREATER_THAN, 'greater_than'],
    [FILTERS.JSON_EQUAL, 'equals'],
    [FILTERS.JSON_LESS_THAN, 'lesser_than']
]);


const JSON_KEYS = new Map([
    [COLUMNS.CHECKBOX, 'selected'],
    [COLUMNS.BENCHMARK, "benchmark"],
    [COLUMNS.SITE, "site"],
    [COLUMNS.UPLOADER, "uploader"],
    [COLUMNS.DATA, "data"],
    [COLUMNS.TAGS, "tags"]
]);

/**
 * The ResultSearch class is responsible to communicate with the backend to 
 * get the search results and string them.
 */
class ResultSearch extends Content {
    constructor() {
        super();
        this.query = "";
        this.results = [];

        this.current_page = 1;
        this.page_count = 1;
        this.filters = [];
        this.results_per_page = 10;
        this.ordered_by = null;
        this.filter_ids = 0;

        this.msg = "";
        this.table = document.getElementById("result_table");
    }

     onload() {
        // Case it got initialed with a Benchmark.
        if (benchmark) {
            this.add_filter_field({ 'filter_type': 'Benchmark', 'input': benchmark });
        }
        this.add_filter_field();
        this.search();
        // Enable popover.
        $('[data-toggle="popover"]').popover({
            html: true
        });
    }

    update() {
        // Update table.
        this.set_result_table();
        this.generate_tag_cont();
        // Update tag info description.
        let filters = document.getElementById("filters").childNodes;
        filters.forEach(function (f) {
            if (f.firstChild && f.firstChild.value && f.firstChild.value.includes("Tag")) {
                // Select the info element, and update content.
                f.childNodes.forEach(function (x) {
                    if (x.getAttribute("id") && x.getAttribute("id").includes("info")) {
                        x.setAttribute("data-content",
                            search_page.generate_tag_cont()
                        );
                    }
                });
            }

        });
        $('[data-toggle="popover"]').popover({
            html: true
        });
    }

    clear_table() {
        while (this.table.firstChild != null) {
            this.table.firstChild.remove();
        }
    }

    display_json(json) {
        let json_block = document.getElementById('jsonPreviewContent').textContent = json;
        //hljs.highlightBlock(json_block);
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block);
        });
        $('#jsonPreviewModal').modal('show');
    }

    create_table_head() {
        let head = document.createElement("THEAD");
        for (const column in COLUMNS) {
            const column_name = COLUMNS[column];

            let cell = document.createElement("TH");
            cell.textContent = column_name;
            cell.setAttribute("scope", "col");

            switch (column_name) {
                case (COLUMNS.CHECKBOX): {
                    // sort by selected results
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => x["selected"] < y["selected"], column_name);
                    });
                } break;
                case (COLUMNS.BENCHMARK): {
                    // alphabetically sort by benchmark
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => x["benchmark"] < y["benchmark"], column_name);
                    });
                } break;
                case (COLUMNS.SITE): {
                    // alphabetically sort by site
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => x["site"] < y["site"], column_name);
                    });
                } break;
                case (COLUMNS.UPLOADER): {
                    // alphabetically sort by uploader
                    cell.addEventListener("click", function () {
                        search_page.sort_by((x, y) => x["uploader"] < y["uploader"], column_name);
                    });
                } break;
                case (COLUMNS.DATA):
                    // Not clear what to sort after.
                    break;
                case (COLUMNS.TAGS):
                    // todo find order on tags
                    break;
                default:
                    break;
            }
            head.appendChild(cell);
        }
        this.table.appendChild(head);
    }

    fill_table () {
        let start = (this.current_page - 1) * this.results_per_page;
        let end = Math.min(start + this.results_per_page, this.results.length);
        for (let i = start; i < end; i++) {
            let row = document.createElement("TR");
            const result = this.results[i];
            // First column ins select box
            for (const key in COLUMNS) {
                const column = COLUMNS[key];
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
                            search_page.select_result(i);
                        });
                        cell.appendChild(select);
                    } break;

                    case (COLUMNS.DATA): {
                        let view_button = document.createElement("input");
                        view_button.setAttribute("type", "submit");
                        view_button.setAttribute("value", "View JSON");
                        view_button.setAttribute("class", "btn btn-secondary btn-sm");
                        view_button.addEventListener("click", function() {
                            search_page.display_json(JSON.stringify(result[JSON_KEYS.get(column)], null, 4));
                        });

                        // set hover-text to content
                        //view_data.setAttribute("title", JSON.stringify(result[column], null, "\t"));
                        cell.appendChild(view_button);
                    } break;
                    case (COLUMNS.SITE):
                    case (COLUMNS.UPLOADER):
                    case (COLUMNS.TAGS):
                    case (COLUMNS.BENCHMARK): {
                        cell.textContent = result[JSON_KEYS.get(column)];
                    } break;
                    case COLUMNS.ACTIONS: {
                        // actions
                        let cell = document.createElement("TD");

                        let div = document.createElement('div');
                        div.classList.add('btn-group');

                        let actions_report = document.createElement("button");
                        actions_report.textContent = 'Report';
                        actions_report.classList.add('btn',  'btn-warning', 'btn-sm');
                        actions_report.setAttribute('type', 'button');
                        actions_report.addEventListener('click', function() {
                            search_page.report_result(result);
                        });
                        div.appendChild(actions_report);

                        if (admin) {
                            let actions_delete = document.createElement('button');
                            actions_delete.textContent = 'Delete';
                            actions_delete.classList.add('btn', 'btn-danger', 'btn-sm');
                            actions_delete.setAttribute('type', 'button');
                            actions_delete.addEventListener('click', function() {
                                search_page.delete_result(result);
                            });
                            div.appendChild(actions_delete);
                        }
                        cell.appendChild(div);
                        row.appendChild(cell);
                    } break;
                }
                row.appendChild(cell);
            }

            this.table.appendChild(row);
        }
    }

    set_result_table() {
        this.clear_table();
        this.create_table_head();
        this.fill_table();
    }

    update_pagination() {
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
        for (let i = 1; i <= this.page_count; i++) {
            // link box
            let new_page_link_slot = document.createElement('li');
            new_page_link_slot.classList.add('page-item');
            // page link button
            let new_page_link = document.createElement('a');
            new_page_link.textContent = i.toString();
            new_page_link.classList.add('page-link');
            new_page_link.addEventListener("click", function() {
                search_page.set_page(i);
            });
            // highlight current page
            if (i === this.current_page) {
                new_page_link_slot.classList.add('active');
            }
            new_page_link_slot.appendChild(new_page_link);
            it.parentElement.insertBefore(new_page_link_slot, next_page_button);
        }

        if (this.current_page <= 1) {
            document.getElementById("prevPageButton").classList.add('disabled');
        }
        else {
            document.getElementById("prevPageButton").classList.remove('disabled');
        }
        if (this.current_page >= this.page_count) {
            document.getElementById("nextPageButton").classList.add('disabled');
        }
        else {
            document.getElementById("nextPageButton").classList.remove('disabled');
        }
    }

    set_page_selection() {
        // Set Page selection to fit the amount of results.
        // Calc amount of pages.
        let pages = (this.results.length - (this.results.length % this.results_per_page)) / this.results_per_page;
        // If div rounded down.
        if ((this.results.length % this.results_per_page) !== 0) {
            pages++;
        }
        // If no result sill page 1 selectable.
        if (pages <= 0) {
            pages = 1;
        }
        this.page_count = pages;

        this.update_pagination();
    }

    /**
     * Go to the previous page.
     */
    prev_page() {
        this.current_page--;
        this.update();
        this.update_pagination();
    }

    /**
     * Go to the specified page.
     * @param page page number
     */
    set_page(page) {
        this.current_page = page;
        this.update();
        this.update_pagination();
    }

    /**
     * Go to the previous page.
     */
    next_page() {
        this.current_page++;
        this.update();
        this.update_pagination();
    }

    search() {
        /** Search the database using selected filters. */
        // Generate query.
        let filters = [];
        let html_filter = document.getElementById("filters").children;
        // Add filters.
        for (let index = 0; index < html_filter.length; index++) {
            let type = html_filter[index].firstChild.value;
            let element = "";
            if (type.includes("Value")) {
                let key = html_filter[index].firstChild.nextSibling.value;
                let value = html_filter[index].firstChild.nextSibling.nextSibling.value;
                // Remove spaces and " characters.
                key = key.replace(/(\s+)/g, '').replace(/"+/g, "'");
                type = FILTER_KEYS.get(type) + "";
                if (key !== "" && value !== "" && type !== "") {
                    element = { 'type': 'json', 'key': key, 'value': value, 'mode': type };

                }
            } else {
                let value = html_filter[index].firstChild.nextSibling.value;
                console.log(type, value);
                type = FILTER_KEYS.get(type);
                console.log(type, value);
                if (type !== "" && value !== "") {
                    element = { 'type': type, 'value': value };
                }
            }
            // Append if not empty
            if (element !== "") {
                filters = filters.concat([element]);
            }
        }
        // Finish query.
        this.query = { "filters": filters };

        document.getElementById('loading-icon').classList.add('loading');

        // Find get new results via ajax query.
        $.ajax('/query_results?query_json=' + encodeURI(JSON.stringify(this.query)))
            .done(function (data) {
                search_page.results = data["results"];
                if (search_page.results.length > 0) {
                    // add selected col
                   search_page.results.forEach(element => {
                        element["selected"] = false;
                    });
                }
                search_page.current_page = 1;
                search_page.set_page_selection();
                search_page.update();
                document.getElementById('loading-icon').classList.remove('loading');
            });
        return false;
    }

        /**Add an filter filed consisting of an selection of filter type,
         * one or tow input fields and the option of removing the created filter field.
         * Args:
         *  input_values: An optional object witch should contain a subset of following attributes
         *                - filter_type (the type of filter, the value should be element of filter_types),
         *                - input (input value of corresponding filter),
         *                - num_input (numeric input value of corresponding filter).
         */
    add_filter_field(input_values) {
        let filter_id = "f" + this.filter_ids++;

        let filter_list = document.getElementById('filters');
        // add line for the filter
        let new_filter = document.createElement('LI');
        new_filter.setAttribute("id", filter_id);
        new_filter.setAttribute("class", "flexbox filter");
        let filter_type = document.createElement("select");
        // add filter types
        for (let filter in FILTERS) {
            // Create options with their name as value.
            let type = document.createElement("OPTION");
            type.setAttribute("value", FILTERS[filter]);
            type.textContent = FILTERS[filter];
            filter_type.appendChild(type);
        }

        // add callback to set type hints
        filter_type.addEventListener("change", function () {
            if (filter_type.value.localeCompare(FILTERS.JSON_LESS_THAN) === 0
                || filter_type.value.localeCompare(FILTERS.JSON_EQUAL) === 0
                || filter_type.value.localeCompare(FILTERS.JSON_GREATER_THAN) === 0) {
                // Give field for numeric value.
                document.getElementById("number" + filter_id).style.visibility = "visible";
                // Set descriptive placeholder.
                document.getElementById("filter_value" + filter_id).placeholder = "path.to.value";
                // Adjust info.
                let info_element = document.getElementById("info" + filter_id);
                info_element.setAttribute("data-content",
                    'The search value has to describe the exact path within the JSON, separated with a dot.\
                    (Only search for numeric values possible.) \
                    <br/> <b>Example:</b> \
                    <br/> <code>{"example":{"nested":{"json":"value"},"different":{"path":{"to":"otherValue"}}} </code> \
                    <br/> <b>Correct:</b> \
                    <br/> example.nested.json or different.path.to \
                    <br/> <b>Wrong:</b> \
                    <br/> json or example.nested or different:path:to'.replace("\n", "<br/>"));
            }
            else {
                // hide value field
                document.getElementById("number" + filter_id).style.visibility = "hidden";
            }
            if (filter_type.value.localeCompare(FILTERS.BENCHMARK) === 0) {
                // Set descriptive placeholder.
                document.getElementById("filter_value" + filter_id).placeholder = "User/Image";
                document.getElementById("info" + filter_id).setAttribute("data-content",
                    'The Benchmark name has to be complete, following the structure <i>Dockerhub username  <b> / </b>Image name </i> . \
                    <br> The <a href="/" >Benchmark search</a> can be used to discover Benchmarks.'
                );
            }
            if (filter_type.value.localeCompare(FILTERS.TAG) === 0) {
                // Set descriptive placeholder.
                document.getElementById("filter_value" + filter_id).placeholder = "SingleTag";
                document.getElementById("info" + filter_id).setAttribute("data-content",
                    search_page.generate_tag_cont()
                );
            }
            if (filter_type.value.localeCompare(FILTERS.UPLOADER) === 0) {
                // Set descriptive placeholder.
                document.getElementById("filter_value" + filter_id).placeholder = "Uploader@provid.er";
                document.getElementById("info" + filter_id).setAttribute("data-content",
                    "The Uploader is described by the uploader's email. Different uploaders can be found in the table below in the <i>Uploader</i> column."
                );
            }
            if (filter_type.value.localeCompare(FILTERS.SITE) === 0) {
                // Set descriptive placeholder.
                document.getElementById("filter_value" + filter_id).placeholder = "Site";
                document.getElementById("info" + filter_id).setAttribute("data-content",
                    'The site requires a single site as input. Sites can be found in the <i>Site</i> column in the result table below.'
                );
            }
        });
        filter_type.setAttribute("class", "form-control");
        // Create input.
        let input = document.createElement("input");
        input.setAttribute("type", "text");
        input.setAttribute("id", "filter_value" + filter_id);
        input.setAttribute("placeholder", "Filter Value");
        input.setAttribute("class", "form-control");
        // Create number field.
        let num_input = document.createElement("input");
        num_input.setAttribute("id", "number" + filter_id);
        num_input.setAttribute("min", "0");
        num_input.setAttribute("class", "form-control");
        num_input.style.visibility = "hidden";
        // Create button to remove given filter.
        let remove_filter = document.createElement("input");
        remove_filter.setAttribute("type", "button");
        remove_filter.setAttribute("class", "btn btn-danger");
        remove_filter.setAttribute("value", "Remove Filter");
        remove_filter.addEventListener("click", function () {
            search_page.remove_filter(filter_id);
        })
        // Create info button.
        let type_info = document.createElement("input");
        type_info.setAttribute("type", "button");
        type_info.setAttribute("id", "info" + filter_id);
        type_info.setAttribute("class", "btn btn-warning");
        type_info.setAttribute("value", "?");
        type_info.setAttribute("data-toggle", "popover");
        type_info.setAttribute("title", "Format Description");
        type_info.setAttribute("data-content", "You find some Tips for the expected input values here.");
        type_info.setAttribute("data-placement", "right");
        // Add default parameters if given.
        if (input_values) {
            if (input_values["filter_type"]) {
                filter_type.value = input_values["filter_type"];
            }
            if (input_values["input"]) {
                input.value = input_values["input"];
            }
            if (input_values["num_input"]) {
                num_input = input_values["num_input"];
            }
        }
        // Add selection to row.
        new_filter.appendChild(filter_type);
        // Add input text field.
        new_filter.appendChild(input);
        // Add numeric input field.
        new_filter.appendChild(num_input);
        // Add remove filter button.
        new_filter.appendChild(remove_filter);
        new_filter.appendChild(type_info);
        filter_list.appendChild(new_filter);
        // Activate popover.
        $('[data-toggle="popover"]').popover({
            html: true
        });
    }

    remove_filter(filter_id) {
        /** Remove the filter*/
        document.getElementById(filter_id).remove();
    }

    sort_by(callback, column) {
        /** Sort result table by a criteria and a given column.
         * Args:
         *     criteria: A function taking tow results and returning a bool, in  a way
         *               a order is defined.
         *     column:   Which column to sort by.
         */
        this.results.sort(callback);
        // reverse order if double clicked.
        if (this.ordered_by === column) {
            this.results = this.results.reverse();
            this.ordered_by = "";
        } else {
            this.ordered_by = column;
        }
        this.update();
    }

    set_results_per_page() {
        /** Reads the selected results per page and updates teh site accordingly. */
        this.results_per_page = document.getElementById("results_on_page").value;
        // Restart at page 1;
        this.current_page = 1;
        this.set_page_selection();
        this.update();
    }

    select_result(result_number) {
        /**Select result if unselected otherwise unselect.*/
        this.results[result_number]["selected"] = !(this.results[result_number]["selected"]);
    }

    open_new_tab(url) {
        window.open(url, '_blank');
    }

    make_diagram() {
        /**Link to the Diagram-page, with selected results.*/
        // Store data in href
        let selected_results = this.results.filter(x => x["selected"]);
        let uuids = "";
        if (selected_results.length > 0) {
            for (let index in selected_results) {
                uuids += "result_uuids=" + selected_results[index]["uuid"] + "&";
            }
        }
        this.open_new_tab('/make_diagram?' + uuids.slice(0, -1));
    }

        /**
         * Helper method generating the tag input field info according to the current results.
         * Returns:
         *      A string containing the html formatted text.
         */
    generate_tag_cont() {
        let msg = "";
        // Collect all tags
        let tags = "";
        for (let i = 0; i < this.results.length; i++) {
            if (this.results[i].tags) {
                tags += this.results[i].tags + ",";
            }
        }
        // Count double tags
        let tag_tuple = {};
        tags.split(",").filter(Boolean).forEach(function (i) { tag_tuple[i] = (tag_tuple[i] || 0) + 1; });
        let tag_tmp = [];
        // Convert to List.
        for (let tag in tag_tuple) {
            tag_tmp.push([tag, tag_tuple[tag]]);
        }
        tag_tmp.sort(function (x, y) {
            return x - y;
        })
        msg = 'The Tag value has to be a single tag.<br>';
        if (this.results.length >= 100) {
            // Most likely not all matching results loaded.
            msg += "The below listed tags and occurrence amount are <b>not representative</b> of the result space.\n";
        } else {
            // All matching results loaded.
            msg += "The list below lists all tags and occurrence amount from the result list matching your query. \n"
        }
        tag_tmp.forEach(function (x) { msg += "<br>" + x[0] + " <i>(" + x[1] + ")</i>"; });
        return msg;
    }

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
}

//
let search_page = null;

window.addEventListener("load", function () {
    search_page = new ResultSearch();
    search_page.onload();
});


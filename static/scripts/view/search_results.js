
// parameters represented as external state, so ResultSearch has no internal state, instead of a mix.
window.addEventListener("load", function () {
    onload();
});


function onload() {
    // initializes state not contained in the html.
    query = "";
    results = [];
    current_page = 1;
    filters = [];
    results_per_page = 10;
    ordered_by = null;
    columns = ["Select", "Benchmark", "Location", "Uploader", "Data", "Tags", "Report"];
    filter_uuid = 0;
    filter_types = ["Benchmark", "Uploader", "Site", "Tag", "Value greater than", "Value equal to", "Value less than"].sort();
    filter_dic = {
        "Benchmark": 'benchmark', "Uploader": "uploader", "Site": "site", "Tag": "tag", "Value greater than": "greater_than",
        "Value equal to": "equals", "Value less than": "lesser_than"
    };
    if (admin) {
        columns.push("Delete");
    }
    values = ["selected", "benchmark", "site", "uploader", "data", "tags"];
    filter_uuid = 0;
    msg = "";

    // Case it got initialed with a Benchmark.
    if (benchmark) {
        ResultSearch.add_filter_field({ 'filter_type': 'Benchmark', 'input': benchmark });
    }
    ResultSearch.add_filter_field();
    ResultSearch.search();
    // Enable popover.
    $('[data-toggle="popover"]').popover({
        html: true
    });
}
/**
 * The ResultSearch class is responsible to communicate with the backend to 
 * get the search results and string them.
 */
class ResultSearch extends Content {


    static update() {
        // Update table.
        this.set_result_table();
        ResultSearch.generate_tag_cont();
        // Update tag info description.
        let filters = document.getElementById("filters").childNodes;
        filters.forEach(function (f) {
            if (f.firstChild && f.firstChild.value && f.firstChild.value.includes("Tag")) {
                // Select the info element, and update content.
                f.childNodes.forEach(function (x) {
                    if (x.getAttribute("id") && x.getAttribute("id").includes("info")) {
                        x.setAttribute("data-content",
                            ResultSearch.generate_tag_cont()
                        );
                    }
                });
            }

        });
        $('[data-toggle="popover"]').popover({
            html: true
        });
    }


    static set_result_table() {
        /**create the result table from current results */
        // Empty existing table.
        var table = document.getElementById("result_table");
        while (table.firstChild != null) {
            table.firstChild.remove();
        }
        // Create head.
        var head = document.createElement("THEAD");
        for (var index in columns) {
            const col = columns[index]
            var cell = document.createElement("TH");
            cell.textContent = col;
            switch (col) {
                case ("Select"):
                    // Sort top if Selected.
                    cell.addEventListener("click", function () {
                        ResultSearch.sort_by((x, y) => x["selected"] < y["selected"], col)
                    });
                    break;
                case ("Benchmark"):
                    // Sort by benchmarks alphabetical.
                    cell.addEventListener("click", function () {
                        ResultSearch.sort_by((x, y) => x["benchmark"] < y["benchmark"], col)
                    });
                case ("Location"):
                    // Sort by location alphabetical.
                    cell.addEventListener("click", function () {
                        ResultSearch.sort_by((x, y) => x["site"] < y["site"], col)
                    });
                    break;
                case ("Uploader"):
                    // Sort by uploader alphabetical.
                    cell.addEventListener("click", function () {
                        ResultSearch.sort_by((x, y) => x["uploader"] < y["uploader"], col)
                    });
                    break;
                case ("Data"):
                    // Not clear what to sort after.
                    break;
                case ("Tags"):
                    // todo find order on tags
                    break;
                default:
                    break;
            }
            head.appendChild(cell);
        }
        table.appendChild(head);
        // Create Body.
        var results_amount = results.length;
        var start = (current_page - 1) * results_per_page;
        var end = Math.min(start + parseInt(results_per_page), results_amount);
        for (var i = start; i < end; i++) {
            var row = document.createElement("TR")
            const res = results[i];
            // First column ins select box
            for (index in values) {
                const col = values[index];
                var cell = document.createElement("TD");
                switch (col) {
                    case ("selected"):
                        var select = document.createElement("input");
                        select.setAttribute("type", "checkbox");
                        select.setAttribute("id", "selected" + i);
                        if (res["selected"]) {
                            // 
                            select.setAttribute("checked", "");
                        }
                        // Event Listener to keep presentation and data in sync.
                        let num = i;// bc js.
                        select.addEventListener("click", function () {
                            ResultSearch.select_result(num);
                        });
                        cell.appendChild(select);
                        break;
                    case ("site"):
                        cell.textContent = res[col];
                        break;
                    case ("uploader"):
                        cell.textContent = res[col];
                        break;
                    case ("data"):
                        var view_data = document.createElement("A");
                        view_data.textContent = "view JSON";
                        let href = "./result" + "?uuid=" + res["uuid"];
                        view_data.setAttribute("href", href);
                        view_data.setAttribute("target", "_blank");
                        view_data.setAttribute("title", JSON.stringify(res[col], null, "\t"));
                        cell.appendChild(view_data);
                        break;
                    case ("tags"):
                        cell.textContent = res[col];
                        break;
                    case ("benchmark"):
                        cell.textContent = res[col];
                        break;
                    default:
                        if (res[col] = ! null) {
                            cell.textContent = res[col];
                        }

                }
                row.appendChild(cell);
            }
            // Add report col
            if (columns.includes("Report")) {
                let cell = document.createElement("TD");
                var report_result = document.createElement("A");
                report_result.textContent = "Report";
                let href = "./report_result" + "?uuid=" + res["uuid"];
                report_result.setAttribute("href", href);
                cell.appendChild(report_result);
                row.appendChild(cell);
            }
            // Add delete col
            if (columns.includes("Delete")) {
                let cell = document.createElement("TD");
                var delete_btn = document.createElement("input");
                delete_btn.setAttribute("type", "submit");
                delete_btn.setAttribute("value", "Delete Result");
                delete_btn.setAttribute("data-toggle", "popover");
                delete_btn.setAttribute("title", "Delete result from system.");
                delete_btn.setAttribute("data-content", "Deleting the result will remove it from the database <b>not (just) the search selection</b>.");
                delete_btn.setAttribute("data-placement", "right");
                delete_btn.setAttribute("data-trigger", "hover");
                delete_btn.setAttribute("class", "btn btn-danger");
                // add delete function
                delete_btn.addEventListener("click", function () {
                    ResultSearch.delete_result(res["uuid"]);
                });
                cell.appendChild(delete_btn);
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
    }
    static set_page_selection() {
        /** Set Page selection to fit the amount of  results.*/
        // Calc amount of pages.
        var pages = (results.length - (results.length % results_per_page))
            / results_per_page;
        // If div rounded down.
        if ((results.length % results_per_page) != 0) {
            pages++;
        }
        // If no result sill page 1 selectable.
        if (pages <= 0) {
            pages = 1;
        }
        // Get pages Selection.
        var pages_select = document.getElementById("pages");
        // Remove Previous options.
        while (pages_select.firstChild != null) {
            pages_select.firstChild.remove();
        }
        // Add the new options.
        for (var i = 1; i <= pages; i++) {
            let p = document.createElement("OPTION");
            p.setAttribute("value", i);
            p.textContent = "Page: " + i;
            p.addEventListener("click", function () {
                ResultSearch.set_page(i);
            });
            pages_select.appendChild(p);
        }

    }
    static set_page() {
        /** Change the page displayed. */
        current_page = document.getElementById("pages").value;
        this.update();
    }

    static search() {
        /** Search the database using selected filters. */
        // Generate query.
        let filters = [];
        var html_filter = document.getElementById("filters").children;
        // Add filters.
        for (var index = 0; index < html_filter.length; index++) {
            let type = html_filter[index].firstChild.value;
            let element = "";
            if (type.includes("Value")) {
                let key = html_filter[index].firstChild.nextSibling.value;
                let value = html_filter[index].firstChild.nextSibling.nextSibling.value;
                // Remove spaces and " characters.
                key = key.replace(/(\s+)/g, '').replace(/\"+/g, "'");
                type = filter_dic[type] + "";
                if (key != "" && value != "" && type != "") {
                    element = { 'type': 'json', 'key': key, 'value': value, 'mode': type };

                }
            } else {
                let value = html_filter[index].firstChild.nextSibling.value;
                type = filter_dic[type];
                if (type != "" && value != "") {
                    element = { 'type': type, 'value': value };
                }
            }
            // Append if not empty
            if (element != "") {
                filters = filters.concat([element]);
            }
        }
        // Finish query.
        query = { "filters": filters };
        // Find get new results via ajax query.
        $.ajax('/query_results?query_json='
            + encodeURI(JSON.stringify(query)))
            .done(function (data) {
                results = data["results"];
                if (results.length > 0) {
                    // add selected col
                    results.forEach(element => {
                        element["selected"] = false;
                    });
                }
                current_page = 1;
                document.getElementById("pages").value = current_page;
                ResultSearch.set_page_selection();
                ResultSearch.update();
            });
        return false;
    }
    static add_filter_field(input_values) {
        /**Add an filter filed consisting of an selection of filter type,
         * one or tow input fields and the option of removing the created filter field.
         * Args:
         *  input_values: An optional object witch should contain a subset of following attributes
         *                - filter_type (the type of filter, the value should be element of filter_types),
         *                - input (input value of corresponding filter),
         *                - num_input (numeric input value of corresponding filter).
         */
        var filter_id = "f" + filter_uuid++;
        // Get the filter section.
        var filter_list = document.getElementById('filters');
        // Creat the new filter.
        var new_filter = document.createElement('LI');
        new_filter.setAttribute("id", filter_id);
        let filter_type = document.createElement("select");
        // Add the different types.
        for (var i = 0; i < filter_types.length; i++) {
            // Create options with their name as value.
            var type = document.createElement("OPTION");
            type.setAttribute("value", filter_types[i]);
            type.textContent = filter_types[i];
            filter_type.appendChild(type);
        }
        // listener to adjust input fields and the associated info.
        filter_type.addEventListener("change", function () {
            if (filter_type.value.includes("Value")) {
                // Give field for numeric value.
                document.getElementById("number" + filter_id).style.visibility = "visible";
                // Set descriptive placeholder.
                document.getElementById("filter_value" + filter_id).placeholder = "path.to.value";
                // Adjust info.
                document.getElementById("info" + filter_id).setAttribute("data-content",
                    "The search value has to describe the exact path within the JSON, separated with a dot. (Only search for numeric values possible.) \
                    <br> <b>Example:</b> \
                    <br> <code>{'example':{'nested':{'json':'value'},'different':{'path':{'to':'otherValue'}}} </code> \
                    <br> <b>Correct:</b> \
                    <br> example.nested.json or different.path.to \
                    <br> <b>Wrong:</b> \
                    <br> json or example.nested or different:path:to").replace("\n", "<br>");
            } else {
                // Hide numeric field.
                document.getElementById("number" + filter_id).style.visibility = "hidden";
            }
            if (filter_type.value.includes("Benchmark")) {
                // Set descriptive placeholder.
                document.getElementById("filter_value" + filter_id).placeholder = "User/Image";
                document.getElementById("info" + filter_id).setAttribute("data-content",
                    'The Benchmark name has to be complete, following the structure <i>Dockerhub username  <b> / </b>Image name </i> . \
                    <br> The <a href="/" >Benchmark search</a> can be used to discover Benchmarks.'
                );
            }
            if (filter_type.value.includes("Tag")) {
                // Set descriptive placeholder.
                document.getElementById("filter_value" + filter_id).placeholder = "SingleTag";
                document.getElementById("info" + filter_id).setAttribute("data-content",
                    ResultSearch.generate_tag_cont()
                );
            }
            if (filter_type.value.includes("Uploader")) {
                // Set descriptive placeholder.
                document.getElementById("filter_value" + filter_id).placeholder = "Uploader@provid.er";
                document.getElementById("info" + filter_id).setAttribute("data-content",
                    "The Uploader is described by the uploader's email. Different uploaders can be found in the table below in the <i>Uploader</i> column."
                );
            }
            if (filter_type.value.includes("Site")) {
                // Set descriptive placeholder.
                document.getElementById("filter_value" + filter_id).placeholder = "Location";
                document.getElementById("info" + filter_id).setAttribute("data-content",
                    'The Location requires a single site as input. Sites can be found in the <i>Location</i> column in the result table below.'
                );
            }
        });
        // Create input.
        var input = document.createElement("input");
        input.setAttribute("type", "text");
        input.setAttribute("id", "filter_value" + filter_id);
        input.setAttribute("placeholder", "Filter Value");
        // Create number field.
        var num_input = document.createElement("input");
        num_input.setAttribute("type", "number");
        num_input.setAttribute("id", "number" + filter_id);
        num_input.setAttribute("min", "0");
        num_input.style.visibility = "hidden";
        // Create button to remove given filter.
        var remove_filter = document.createElement("input");
        remove_filter.setAttribute("type", "button");
        remove_filter.setAttribute("class", "btn btn-danger");
        remove_filter.setAttribute("value", "Remove Filter");
        remove_filter.addEventListener("click", function () {
            ResultSearch.remove_filter(filter_id);
        })
        // Create info button.
        var type_info = document.createElement("input");
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

    static remove_filter(filter_id) {
        /** Remove the filter*/
        document.getElementById(filter_id).remove();
    }

    static sort_by(criteria, column) {
        /** Sort result table by a criteria and a given column.
         * Args:
         *     criteria: A function taking tow results and returning a bool, in  a way
         *               a order is defined.
         *     column:   Which column to sort by.
         */
        results.sort(
            criteria
        )
        // reverse order if double clicked.
        if (ordered_by == column) {
            results = results.reverse();
            ordered_by = "";
        } else {
            ordered_by = column;
        }
        this.update();
    }

    static set_results_per_page() {
        /** Reads the selected results per page and updates teh site accordingly. */
        results_per_page = document.getElementById("results_on_page").value;
        // Restart at page 1;
        current_page = 1;
        this.set_page_selection();
        this.update();
    }

    static select_result(result_number) {
        /**Select result if unselected otherwise unselect.*/
        results[result_number]["selected"] = !(results[result_number]["selected"]);
    }


    static make_diagram() {
        /**Link to the Diagram-page, with selected results.*/
        // Store data in href
        let selected_results = results.filter(x => x["selected"]);
        let uuids = "";
        if (selected_results.length > 0) {
            for (var index in selected_results) {
                uuids += "result_uuids=" + selected_results[index]["uuid"] + "&";
            }
        }
        window.location.href = '/make_diagram?' + uuids.slice(0, -1);
    }

    static generate_tag_cont() {
        /**
         * Helper method generating the tag input field info according to the current results.
         * Returns:
         *      A string containing the html formatted text.
         */
        var msg = "";
        // Collect all tags
        let tags = "";
        for (var i = 0; i < results.length; i++) {
            if (results[i].tags) {
                tags += results[i].tags + ",";
            }
        }
        // Count double tags
        var tag_tuple = {};
        tags.split(",").filter(Boolean).forEach(function (i) { tag_tuple[i] = (tag_tuple[i] || 0) + 1; });
        var tag_tmp = [];
        // Convert to List.
        for (var tag in tag_tuple) {
            tag_tmp.push([tag, tag_tuple[tag]]);
        }
        tag_tmp.sort(function (x, y) {
            return x - y;
        })
        msg = 'The Tag value has to be a single tag.<br>';
        if (results.length >= 100) {
            // Most likely not all matching results loaded.
            msg += "The below listed tags and occurrence amount are <b>not representative</b> of the result space.\n";
        } else {
            // All matching results loaded.
            msg += "The list below lists all tags and occurrence amount from the result list matching your query. \n"
        }
        tag_tmp.forEach(function (x) { msg += "<br>" + x[0] + " <i>(" + x[1] + ")</i>"; });
        return msg;
    }

    static delete_result(result) {
        /**Send ajax to remove a specific result form the database.
         * Args:
         *      result: The uuid of a result to be deleted.
         */
        $.ajax('/delete_result?uuid=' + encodeURI(result)).done(function (data) {
            alert(data);
            if (data.toLowerCase.includes("success")) {
                results.filter(function (r) {
                    return r["uuid"] == result;
                });
                ResultSearch.update();
            }
        });
        return false;
    }
}
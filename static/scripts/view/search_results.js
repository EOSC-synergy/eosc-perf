// parameters represented as external state, so ResultSearch has no internal state, instead of a mix.
function onload() {
    query = ""
    results = []
    current_page = 1
    selected_results = []
    admin = true
    filters = []
    results_per_page = 10
    ordered_by = null
    columns = ["Select", "Location", "Uploader", "Json", "Tags", "Report"]
    if (admin) {
        columns.push("Delete");
    }
    values = ["selected", "site", "uploader", "json", "tag"]
    filter_uuid = 0
    filter_types = ["Uploader", "Site", "Tag", "Value greater than", "Value equal to", "Value less than"]
    results = [{
        selected: false, benchmark: "Test Benchmark for cpu", uploader: "John Doe", site: "Paris"
        , tag: "CPU , not GPU", json: { test: "val1", test2: "val2" , uuid:"123"}
    },{
        selected: false, benchmark: "Test Benchmark for cpu", uploader: "John Doe", site: "moon"
        , tag: "CPU , not GPU", json: { test: "val1", test2: "val2" , uuid:"122"}
    }];
    ResultSearch.set_result_table();
    ResultSearch.set_page_selection();
}
/**
 * The ResultSearch class is responsible to communicate with the backend to 
 * get the search results and string them.
 */
class ResultSearch extends Content {

    // add listener to add filter button

    static update() {
        // Update table.
        this.set_result_table();

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
                case ("Json"):
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
        var end = Math.min(start + results_per_page, results_amount);
        console.log("start:"+start+" end:"+end);
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
                    case ("json"):
                        var json = JSON.stringify(res[col]);
                        cell.textContent = json;
                        break;
                    case ("tag"):
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
                let href = "./report_result" + "?uuid=" + res["json"]["uuid"];
                report_result.setAttribute("href", href);
                cell.appendChild(report_result);
                row.appendChild(cell);
            }
            // Add delete col
            if (columns.includes("Delete")) {
                let cell = document.createElement("TD");
                var delete_result = document.createElement("FORM");
                delete_result.setAttribute("method", "post");
                delete_result.setAttribute("id", ("delete" + i));
                var delete_btn = document.createElement("input");
                delete_btn.setAttribute("type", "submit");
                delete_btn.setAttribute("value", "Delete Result");
                delete_btn.setAttribute("class", "btn btn-danger");
                let href = "./report_result" + "?uuid=" + res["json"]["uuid"];
                delete_btn.setAttribute("href", href);
                delete_result.appendChild(delete_btn);
                cell.appendChild(delete_result);
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
        current_page = document.getElementById("pages").value;
        this.update();
    }

    static search(new_query) {
        // Generate query.

        // Request the result query.
        $.getJSON('/query_results', { 'query_json': JSON.stringify(query) },
            function (data) { results = JSON.parse(data.result) });

    }
    static add_filter_field() {
        var filter_id = "f" + filter_uuid++;
        // Get the filter section.
        var filter_list = document.getElementById('filters');
        // Creat the new filter.
        var new_filter = document.createElement('LI');
        new_filter.setAttribute("id", filter_id);
        var filter_type = document.createElement("select");
        // Add the different types.
        for (var i = 0; i < filter_types.length; i++) {
            // Create options with their name as value.
            var type = document.createElement("OPTION");
            type.setAttribute("value", filter_types[i]);
            type.textContent = filter_types[i];
            filter_type.appendChild(type);
        }
        // Add selection to row
        new_filter.appendChild(filter_type);
        // Create input.
        var input = document.createElement("input");
        input.setAttribute("type", "text");
        input.setAttribute("placeholder", "Filter Value");
        new_filter.appendChild(input);
        // Create button to remove given filter.
        var remove_filter = document.createElement("input");
        remove_filter.setAttribute("type", "button");
        remove_filter.setAttribute("value", "Remove Filter");
        remove_filter.addEventListener("click", function () {
            ResultSearch.remove_filter(filter_id);
        })
        new_filter.appendChild(remove_filter);
        filter_list.appendChild(new_filter);
    }

    static remove_filter(filter_id) {
        // Remove the filter
        document.getElementById(filter_id).remove()
    }

    static sort_by(criteria, column) {
        results.sort(
            criteria
        )
        // reverse order if double clicked.
        if (ordered_by == column) {
            results = results.reverse()
        }
        ordered_by = column
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
        // Store data in href
    }

    static delete_result(result) {

    }

    static report_result(result) {

    }

    static result_information(result) {

    }

    static hide_information(result) {

    }

}
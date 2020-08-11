/**
 * The ResultSearch class is responsible to communicate with the backend to 
 * get the search results and string them.
 */

class ResultSearch extends Content {

    query = ""
    results = []
    current_page = 1
    selected_results = []
    admin = false
    filters = []
    results_per_page = 10
    ordered_by = null
    columns = ["Selected", "Benchmark", "Uploader", "Location", "Tags", "Json", "Report"]
    values = ["benchmark", "uploader", "site", "tag", "json"]

    static update() {
        // Update table. 
        const creat_cell = (value, type) => "<" + type + ">" + value + "</" + type + ">\n"
        const create_row = (row, type) => "<tr>\n" +
            row.map(x => create_cell(x, type))
                .reduce((x, y) => x + y) + "</tr>\n";
        // Create table head.
        var table_str = create_row(columns, "th")
        // Create table body.
        // Calculate range.
        var results_amount = results.length() - 1
        var start = Math.min((current_page - 1) * results_per_page, results_amount)
        var end = Math.min(start + results_per_page, results_amount)
        for (var i = start; i < end; i++) {
            table_str += "<tr>\n"
            // Add select field.
            if (results["selected"]) {
                var box = "<input type=\"checkbox\" id = \"s" + i + "\">"
                table_str += creat_cell(box, "td")
            } else {

            }
            // Add the values.
            for (var value = 0; value < values.length; value++) {
                table_str += create_cell(results[i][values[j]], "td")
            }
            table_str += "</tr>\n"
        }
        // Set table in html.
        $("#result_page").html(table_str);

    }
    static set_page(page) {
        current_page = page
        update()
    }

    static search(new_query) {
        // Generate query.
        // Request the result query.
        $.getJSON('/query_results', { 'query_json': JSON.stringify(query) },
            function (data) { results = JSON.parse(data.result) })
        // Add select field.
        results = results.map(result => result["selected"] = false)
    }

    static add_filter(filter) {
        filters.push(filter)
    }

    static remove_filter(filter) {
        filters = filters.filter(function (item) { item !== filter })
    }

    static sort_by(colum) {

        results.sort(
            //todo
        )
        // reverse order if double clicked.
        if (ordered_by == colum) {
            results = results.reverse()
        }
        ordered_by = colum
        update()
    }

    static set_results_per_page(amount) {
        results_per_page = amount
        update()
    }

    static select_result(result) {
        for (var i; i < results; i++) {
            if (results[i] == result) {
                selected_results.push(results[i])
                break
            }
        }
    }

    static unselect_result(result) {
        select_result = select_result.filter(function (item) { item !== filter })
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
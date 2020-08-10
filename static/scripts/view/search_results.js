/**
 * The ResultSearch class is responsible to communicate with the backend to 
 * get the search results and string them.
 */

class ResultSearch extends Content {
    constructor() {
        this.query = ""
        this.results = []
        this.current_page = 1
        this.selected_results = []
        this.admin = false
        this.filters = []
        this.results_per_page = 10
        this.ordered_by = null
        this.columns = ["Benchmark", "Uploader", "Location", "Tags", "Json", "Report"]
        this.values = ["benchmark", "uploader", "site", "tag", "json"]
    }
    update() {
        // Update table. 
        const creat_cell = (value, type) => "<" + type + ">" + value + "</" + type + ">\n"
        const create_row = (row, type) => "<tr>\n" +
            row.map(x => create_cell(x, type))
                .reduce((x, y) => x + y) + "</tr>\n";
        // Create table head.
        var table_str = create_row(this.columns, "th")
        // Create table body.
        // Calculate range.
        var results_amount = this.results.length() - 1
        var start = Math.min((this.current_page - 1) * this.results_per_page, results_amount)
        var end = Math.min(start + this.results_per_page, results_amount)
        for (var i = start; i < end; i++) {
            table_str += "<tr>\n"
            // Add the values.
            for (var value = 0; value < this.values.length; value++) {
                table_str += create_cell(this.results[i][this.values[j]],"td")
            }
            table_str += "</tr>\n"
        }
        // Set table in html.
        $('#result_page').html(table_str)

    }
    set_page(page) {
        this.current_page = page
        this.update()
    }

    search(new_query) {
        // Generate query.
        // Request the result query.
        $.getJSON('/query_results', { 'query_json': JSON.stringify(this.query) },
            function (data) { this.results = JSON.parse(data.result) })
    }

    add_filter(filter) {
        this.filters.push(filter)
    }

    remove_filter(filter) {
        this.filters = this.filters.filter(function (item) { item !== filter })
    }

    sort_by(colum) {

        this.results.sort(
            //todo
        )
        // reverse order if double clicked.
        if (this.ordered_by == colum) {
            this.results = this.results.reverse()
        }
        this.ordered_by = colum
        this.update()
    }

    set_results_per_page(amount) {
        this.results_per_page = amount
        this.update()
    }

    select_result(result) {
        for (var i; i < this.results; i++) {
            if (this.results[i] == result) {
                this.selected_results.push(this.results[i])
                break
            }
        }
    }

    unselect_result(result) {
        this.select_result = this.select_result.filter(function (item) { item !== filter })
    }

    make_diagram() {
        // Store data in href
    }

    delete_result(result) {

    }

    report_result(result) {

    }

    result_information(result) {

    }

    hide_information(result) {

    }
}
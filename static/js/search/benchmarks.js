"use strict";

class BenchmarkSearch {
    constructor() {
        this.hide_nav_buttons();
        this.resultsPerPage = 25;
        this.results = [];
        this.page = 0;

        let form = $('#form');
        form.submit(function (e) {
            benchmarkSearch.search(form.find('input[name="query"]').val().trim());
            return false;
        });

        this.loadingIcon = document.getElementById("loadingIcon");
        this.tableBody = document.getElementById("resultTableBody");
        document.getElementById("pageIndex").style.display = "inline-block";
    }

    show_nav_buttons() {
        document.getElementById("next_button").style.display = "inline-block";
        document.getElementById("previous_button").style.display = "inline-block";
    }

    hide_nav_buttons() {
        document.getElementById("next_button").style.display = "none";
        document.getElementById("previous_button").style.display = "none";
    }

    update_result_table() {
        // clear result
        clear_element_children(this.tableBody);

        let startIndex = this.resultsPerPage * this.page;
        let limit = Math.min(this.results.length, startIndex + 25);

        if (this.results.length === 0) {
            let warning = document.createElement("p");
            warning.classList.add("text-center");
            warning.textContent = "No benchmarks found.";
            this.tableBody.appendChild(warning);
        }
        for (let index = startIndex; index < limit; ++index) {
            let resultRow = this.tableBody.insertRow(-1);
            let dockerNameCell = resultRow.insertCell(0);
            let dockerName = this.results[index].docker_name;

            // add a 'a' with href
            let a = document.createElement('a');
            a.textContent = dockerName;
            a.title = dockerName;
            a.href = '/result_search?benchmark=' + encodeURI(dockerName);
            dockerNameCell.appendChild(a);

            let description = document.createElement("div");
            description.textContent = this.results[index].description;
            dockerNameCell.appendChild(description);
        }
        if (this.results.length > this.resultsPerPage) {
            this.show_nav_buttons();
            let pageAmount = (Math.ceil(this.results.length / this.resultsPerPage));
            document.getElementById("pageIndex").textContent = "Page " + (this.page + 1) + " of " + pageAmount;
        } else {
            this.hide_nav_buttons();
            document.getElementById("pageIndex").textContent = "";
        }
    }

    search(query = "") {
        this.results = [];
        this.page = 0;
        let keywords = query.trim().length > 0 ? query.trim().split(" ") : [];
        this.loadingIcon.classList.add("loading");
        $.ajax('/query_benchmarks?query='
            + encodeURI(JSON.stringify({ 'keywords': keywords })))
            .done(function (data) {
                benchmarkSearch.results = data.results;
                benchmarkSearch.update_result_table();
                benchmarkSearch.loadingIcon.classList.remove("loading");
            });
    }

    prev_page() {
        this.page = Math.max(this.page - 1, 0);
        this.update_result_table();
    }

    next_page() {
        this.page = Math.min(Math.ceil(this.results.length / this.resultsPerPage), this.page + 1);
        this.update_result_table();
    }
}

let benchmarkSearch = null;

window.onload = function () {
    benchmarkSearch = new BenchmarkSearch();
    benchmarkSearch.search();
}

let results_per_page = 25;
let results = [];
let result_amount = 0;
let page = 0;

$(function () {
    let form = $('#form');
    form.submit(function (e) {
        search_benchmarks(form.find('input[name="query"]').val().trim());
        return false;
    });
});

function search_benchmarks(query) {
    results = [];
    result_amount = 0;
    page = 0;
    let keywords = query.split(" ");
    $.ajax('/query_benchmarks?query_json='
        + encodeURI(JSON.stringify({ 'keywords': keywords })))
        .done(function (data) {
            results = data.results;
            result_amount = results.length;
            update_result_table();
        });
}

function update_result_table() {
    // clear result
    let table_body = document.getElementById("result_table_body");
    table_body.innerHTML = '';
    let start_index = results_per_page * page;
    let limit = Math.min(result_amount, start_index + 25);
    if (result_amount === 0) {
        table_body.innerHTML = '<p class="text-center">No benchmarks found.</p>';
    }
    for (let index = start_index; index < limit; ++index) {
        let result_row = table_body.insertRow(-1);
        let docker_name_cell = result_row.insertCell(0);
        let docker_name = results[index].docker_name;

        // add a 'a' with href
        let a = document.createElement('a');

        let link_text = document.createTextNode(docker_name);
        a.appendChild(link_text);
        a.title = docker_name;
        a.href = '/result_search?benchmark=' + encodeURI(docker_name);

        docker_name_cell.appendChild(a);
    }
    if (result_amount > results_per_page) {
        show_nav_buttons();
        let amount_pages = (Math.floor(result_amount / results_per_page) + 1);
        document.getElementById("page_info").innerHTML = "Page " + (page + 1) + " of " + amount_pages;
    } else {
        hide_nav_buttons();
        document.getElementById("page_info").innerHTML = "";
    }
}

function prev_page() {
    if (page > 0) {
        page = page - 1;
    }
    update_result_table();
}

function next_page() {
    if ((page + 1) * results_per_page < result_amount) {
        page = page + 1;
    }
    update_result_table();
}

function hide_nav_buttons() {
    document.getElementById("next_button").style.display = "none";
    document.getElementById("previous_button").style.display = "none";
}

function show_nav_buttons() {
    document.getElementById("next_button").style.display = "inline-block";
    document.getElementById("previous_button").style.display = "inline-block";
}

window.onload = function () {
    hide_nav_buttons();
    document.getElementById("page_info").style.display = "inline-block";
    search_benchmarks("")
}

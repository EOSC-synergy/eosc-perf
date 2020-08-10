$(function () {
    form = $('#form');
    form.submit(function (e) {
        query = form.find('input[name="query"]').val().trim();
        if (query === "") {
            return false;
        }
        table = document.getElementById("result_table");
        keywords = query.split(" ");
        $.ajax('/query_benchmarks?query_json='
            + encodeURI(JSON.stringify(
                {'keywords':keywords})))
            .done(function(data) {
                results = data.results;
                for (index = 0; index < results.length; ++index) {
                    var result_row = table.insertRow(-1)
                    var docker_name_cell = result_row.insertCell(0)
                    var docker_name = results[index].docker_name
                    docker_name_cell.innerHTML = docker_name
                }
                console.log(data);
            })
        return false;
    });
});

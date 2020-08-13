$(function () {
    form = $('#form');
    form.submit(function (e) {
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: new FormData(this),
            dataType: "json",
            success: function (data, textStatus) {
                // display success message and disable form
                console.log("success callback")
                console.log(data)
                $('#overlay-text').text('Submission successful');
                $('#overlay').show();
                $('#form input[type="submit"]').prop("disabled", true);
            },
            error: function (data) {
                console.log("fail callback")
                console.log(data)
                window.location.href = data.responseJSON.redirect;
            }
        });

        return false;
    });
});

function prepare_sites() {
    var site_selection = document.getElementById("site_selection")
    site_selection.innerHTML = ''
    $.ajax('/fetch_sites')
    .done(function(data) {
        console.log(data);
        var sites = data.results;
        for (index = 0; index < sites.length; ++index) {
            site_name = sites[index].name;
            site_id = sites[index].short_name;
            site_html = "<option id=" + site_id + ">" + site_name + "</option>\n" ;
            site_selection.innerHTML += site_html;
        }
        if (sites.length === 0) {
            document.getElementById("submit_button").setAttribute("disabled", true)
        }
    })
}

function prepare_tags() {
    var tag_selection = document.getElementById("tag_selection")
    tag_selection.innerHTML = '<option selected>--No Tag--</option>'
    $.ajax('/fetch_tags')
    .done(function(data) {
        var tags = data.results;
        for (index = 0; index < tags.length; ++index) {
            tag_html = "<option>" + tags[index].name + "</option>\n" ;
            tag_selection.innerHTML += tag_html;
        }
        console.log(data);
    })
}

function prepare_benchmarks() {
    var bm_selection = document.getElementById("bm_selection")
    $.ajax('/fetch_benchmarks')
    .done(function(data) {
        console.log(data);
        var benchmarks = data.results;
        for (index = 0; index < benchmarks.length; ++index) {
            benchmark_html = "<option>" + benchmarks[index].docker_name + "</option>\n";
            bm_selection.innerHTML += benchmark_html;
        }
        if (benchmarks.length === 0) {
            document.getElementById("submit_button").setAttribute("disabled", true)
        }
    })
}

window.onload = function() {
    prepare_sites()
    prepare_tags()
    prepare_benchmarks()
}

function before_submit(){
    // Switch human readable long name of site with unique short name
    var selection = document.getElementById('site_selection');
    var site_id = selection.options[selection.selectedIndex].id;
    console.log(site_id)
    selection.options[selection.selectedIndex].innerHTML = site_id
    return true;
}
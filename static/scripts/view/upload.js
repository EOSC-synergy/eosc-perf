var SITES_EMPTY = true
var BENCHMARKS_EMPTY = true

$(function () {
    form = $('#form');
    form.submit(function (e) {
        var selection = document.getElementById('site_selection');
        var site_id = selection.options[selection.selectedIndex].id;
        selection.options[selection.selectedIndex].innerHTML = site_id;

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: new FormData(this),
            processData: false,
            contentType: false,
            success: function (data, textStatus) {
                // display success message and disable form
                $('#overlay-text').text('Submission successful');
                $('#overlay').show();
                (function ($) {
                    $('#overlay').on('click', function (e) {
                        if (e.target !== this)
                            return;
                        $(this).fadeOut();
                        document.getElementById("result_file").value = "";
                        document.getElementById("agreed_license").checked = false
                        $('#form input[type="submit"]').prop("disabled", true);
                    });
                })(jQuery);
            },
            error: function (data) {
                window.location.href = data.responseJSON.redirect;
            }
        });

        return false;
    });
});

function license_checkbox_click(cb) {
    if (cb.checked && !(SITES_EMPTY || BENCHMARKS_EMPTY)) {
        document.getElementById("submit_button").removeAttribute("disabled")
    } else {
        document.getElementById("submit_button").setAttribute("disabled", true);
    }
}

function show_license() {
    license = document.getElementById("license").getAttribute("value");
    var wnd = window.open("about:blank", "", "_blank");
    wnd.document.write("<html><body>"+license+"</body></html>");
}

function prepare_sites() {
    var site_selection = document.getElementById("site_selection");
    site_selection.innerHTML = '';
    $.ajax('/fetch_sites')
        .done(function (data) {
            var sites = data.results;
            for (index = 0; index < sites.length; ++index) {
                site_name = sites[index].name;
                site_id = sites[index].short_name;
                site_html = "<option id=" + site_id + ">" + site_name + "</option>\n";
                site_selection.innerHTML += site_html;
            }
            if (sites.length === 0) {
                SITES_EMPTY = true
                document.getElementById("submit_button").setAttribute("disabled", true)
            }
        })
}

function prepare_tags() {
    var tag_selection = document.getElementById("tag_selection")
    tag_selection.innerHTML = '<option selected>--No Tag--</option>'
    $.ajax('/fetch_tags')
        .done(function (data) {
            var tags = data.results;
            for (index = 0; index < tags.length; ++index) {
                tag_html = "<option>" + tags[index].name + "</option>\n";
                tag_selection.innerHTML += tag_html;
            }
        })
}

function prepare_benchmarks() {
    var bm_selection = document.getElementById("bm_selection")
    $.ajax('/fetch_benchmarks')
        .done(function (data) {
            var benchmarks = data.results;
            for (index = 0; index < benchmarks.length; ++index) {
                benchmark_html = "<option>" + benchmarks[index].docker_name + "</option>\n";
                bm_selection.innerHTML += benchmark_html;
            }
            if (benchmarks.length === 0) {
                BENCHMARKS_EMPTY = true
                document.getElementById("submit_button").setAttribute("disabled", true)
            }
        })
}

window.onload = function () {
    prepare_sites()
    prepare_tags()
    prepare_benchmarks()
}

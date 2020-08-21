var SITES_EMPTY = false
var BENCHMARKS_EMPTY = false
var CUSTOM_SITE = false
var LICENSE_AGREED = false

$(function () {
    form = $('#form');
    form.submit(function (e) {
        var selection = document.getElementById('site_selection');
        var old_html = selection.options[selection.selectedIndex].innerHTML
        var site_id = selection.options[selection.selectedIndex].id;
        selection.options[selection.selectedIndex].innerHTML = site_id;
        formData = new FormData(this)
        append_form_data(formData)
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            success: function (data, textStatus) {
                // display success message and reset page
                $('#overlay-text').text('Submission successful');
                $('#overlay').show();
                prepare_page()
            },
            error: function (data) {
                window.location.href = data.responseJSON.redirect;
            }
        });
        selection.options[selection.selectedIndex].innerHTML = old_html;
        return false;
    });
});

function site_checkbox_click(cb) {
    CUSTOM_SITE = cb.checked;
    if (CUSTOM_SITE) {
        document.getElementById("site_name").removeAttribute("disabled");
        document.getElementById("site_address").removeAttribute("disabled");
        document.getElementById("site_description").removeAttribute("disabled");
        document.getElementById("site_selection").setAttribute("disabled", true);
        if (!BENCHMARKS_EMPTY && LICENSE_AGREED) {
            document.getElementById("submit_button").removeAttribute("disabled");
        }
    } else {
        document.getElementById("site_name").setAttribute("disabled", true);
        document.getElementById("site_name").value = "";
        document.getElementById("site_address").setAttribute("disabled", true);
        document.getElementById("site_address").value = "";
        document.getElementById("site_description").setAttribute("disabled", true);
        document.getElementById("site_description").value = "";
        document.getElementById("site_selection").removeAttribute("disabled");
        if (SITES_EMPTY) {
            document.getElementById("submit_button").setAttribute("disabled", true);
        }
    }
}

function license_checkbox_click(cb) {
    LICENSE_AGREED = cb.checked
    if (LICENSE_AGREED && (!SITES_EMPTY || CUSTOM_SITE) && !BENCHMARKS_EMPTY) {
        document.getElementById("submit_button").removeAttribute("disabled");
    } else {
        document.getElementById("submit_button").setAttribute("disabled", true);
    }
}

function show_license() {
    license = document.getElementById("license").getAttribute("value");
    var wnd = window.open("about:blank", "", "_blank");
    wnd.document.write("<html><body>"+license+"</body></html>");
}

function append_form_data(fd) {
    fd.append("custom_site", CUSTOM_SITE)
    if (CUSTOM_SITE) {
        fd.append("new_site_name", document.getElementById("site_name").value)
        fd.append("new_site_address", document.getElementById("site_address").value)
        fd.append("new_site_description", document.getElementById("site_description").value)
    }
}

function stopped_typing_tag_field(){
    if(document.getElementById("custom_tag").value.trim().length > 0) {
        document.getElementById('add_tag_button').removeAttribute("disabled");
    } else {
        document.getElementById('add_tag_button').setAttribute("disabled", true);
    }
}

function add_tag() {
    tag = document.getElementById("custom_tag").value.trim();
    form = $('#form');
    formData = new FormData()
    formData.append("new_tag", tag)
    $.ajax({
        type: "POST",
        url: "upload_tag",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data, textStatus) {
            // reset tag field and reload tags
            document.getElementById("custom_tag").value  = ""
            document.getElementById('add_tag_button').setAttribute("disabled", true);
            prepare_tags();
        },
        error: function (data) {
            window.location.href = data.responseJSON.redirect;
        }
    });

    form.submit(function (e) {
        var selection = document.getElementById('site_selection');
        var old_html = selection.options[selection.selectedIndex].innerHTML
        var site_id = selection.options[selection.selectedIndex].id;
        selection.options[selection.selectedIndex].innerHTML = site_id;
        formData = new FormData(this)
        append_form_data(formData)
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            success: function (data, textStatus) {
                // display success message and disable form
                $('#overlay-text').text('Submission successful');
                $('#overlay').show();
                prepare_page()
            },
            error: function (data) {
                window.location.href = data.responseJSON.redirect;
            }
        });
        selection.options[selection.selectedIndex].innerHTML = old_html;
        return false;
    });
}

function prepare_sites() {
    var site_selection = document.getElementById("site_selection");
    site_selection.innerHTML = "";
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
                SITES_EMPTY = true;
                document.getElementById("submit_button").setAttribute("disabled", true);
            }
        })
}

function prepare_tags() {
    var tag_selection = document.getElementById("tag_selection");
    tag_selection.innerHTML = '<option selected>--No Tag--</option>';
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
    var bm_selection = document.getElementById("bm_selection");
    bm_selection.innerHTML = "";
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

function prepare_page() {
    document.getElementById("result_file").value = "";
    document.getElementById("custom_tag").value = "";
    document.getElementById('add_tag_button').setAttribute("disabled", true);
    if (false != document.getElementById("agreed_license").checked) {
        document.getElementById("agreed_license").click();
    }
    if (false != document.getElementById("custom_site").checked) {
        document.getElementById("custom_site").click();
    }
    prepare_sites()
    prepare_tags()
    prepare_benchmarks()
}


window.onload = prepare_page
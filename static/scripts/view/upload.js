var SITES_EMPTY = false
var BENCHMARKS_EMPTY = false
var CUSTOM_SITE = false
var LICENSE_AGREED = false

$(function () {
    let form = $('#form');
    form.submit(function (e) {
        let old_html = "";
        if (!CUSTOM_SITE) {
            let selection = document.getElementById('site_selection');
            old_html = selection.options[selection.selectedIndex].innerHTML;
            selection.options[selection.selectedIndex].innerHTML = selection.options[selection.selectedIndex].id;
        }
        let formData = new FormData(this);
        append_form_data(formData);
        submit_form(form, formData,
            function (data, textStatus) {
                // display success message and reset page
                display_message('Submission successful');
                prepare_page();
            },
            function (data) {
                window.location.href = data.responseJSON.redirect;
            });
        if (!CUSTOM_SITE) {
            selection.options[selection.selectedIndex].innerHTML = old_html;
        }
        return false;
    });
});

function site_checkbox_click(cb) {
    CUSTOM_SITE = cb.checked;
    if (CUSTOM_SITE) {
        document.getElementById("site_name").removeAttribute("disabled");
        document.getElementById("site_address").removeAttribute("disabled");
        document.getElementById("site_description").removeAttribute("disabled");
        document.getElementById("site_selection").setAttribute("disabled", "true");
        if (!BENCHMARKS_EMPTY && LICENSE_AGREED) {
            document.getElementById("submit_button").removeAttribute("disabled");
        }
    } else {
        document.getElementById("site_name").setAttribute("disabled", "true");
        document.getElementById("site_name").value = "";
        document.getElementById("site_address").setAttribute("disabled", "true");
        document.getElementById("site_address").value = "";
        document.getElementById("site_description").setAttribute("disabled", "true");
        document.getElementById("site_description").value = "";
        document.getElementById("site_selection").removeAttribute("disabled");
        if (SITES_EMPTY) {
            document.getElementById("submit_button").setAttribute("disabled", "true");
        }
    }
}

function license_checkbox_click(cb) {
    LICENSE_AGREED = cb.checked
    if (LICENSE_AGREED && (!SITES_EMPTY || CUSTOM_SITE) && !BENCHMARKS_EMPTY) {
        document.getElementById("submit_button").removeAttribute("disabled");
    } else {
        document.getElementById("submit_button").setAttribute("disabled", "true");
    }
}

function show_license() {
    let license = document.getElementById("license").getAttribute("value");
    let new_window = window.open("about:blank", "", "_blank");
    new_window.document.write("<html lang=\"en\"><body>"+license+"</body></html>");
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
        document.getElementById('add_tag_button').setAttribute("disabled", "true");
    }
}

function add_tag() {
    let tag = document.getElementById("custom_tag").value.trim();
    let form = $('#form');
    let formData = new FormData();
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
            document.getElementById('add_tag_button').setAttribute("disabled", "true");
            prepare_tags();
        },
        error: function (data) {
            window.location.href = data.responseJSON.redirect;
        }
    });

    form.submit(function (e) {
        let selection = document.getElementById('site_selection');
        let old_html = selection.options[selection.selectedIndex].innerHTML
        selection.options[selection.selectedIndex].innerHTML = selection.options[selection.selectedIndex].id;
        let formData = new FormData(this);
        append_form_data(formData);
        submit_form(form, formData,
            function (data, textStatus) {
                // display success message and disable form
                display_message('Submission successful');
                prepare_page();
            },
            function (data) {
                window.location.href = data.responseJSON.redirect;
            });
        selection.options[selection.selectedIndex].innerHTML = old_html;
        return false;
    });
}

function show_mandatory_fields() {
    
}

function prepare_sites() {
    let site_selection = document.getElementById("site_selection");
    site_selection.innerHTML = "";
    $.ajax('/fetch_sites')
        .done(function (data) {
            let sites = data.results;
            for (let index = 0; index < sites.length; ++index) {
                let site_name = sites[index].name;
                let site_id = sites[index].short_name;
                let site_html = "<option id=" + site_id + ">" + site_name + "</option>\n";
                site_selection.innerHTML += site_html;
            }
            if (sites.length === 0) {
                SITES_EMPTY = true;
                document.getElementById("submit_button").setAttribute("disabled", "true");
            }
        })
}

function prepare_tags() {
    let tag_selection = document.getElementById("tag_selection");
    tag_selection.innerHTML = '<option selected>--No Tag--</option>';
    $.ajax('/fetch_tags')
        .done(function (data) {
            let tags = data.results.sort(compare);
            for (let index = 0; index < tags.length; ++index) {
                let tag_html = "<option>" + tags[index].name + "</option>\n";
                tag_selection.innerHTML += tag_html;
            }
        })
}

// Used to compare tags by their name
function compare(a, b) {
    if (a.name.toLowerCase() < b.name.toLowerCase()){
        return -1;
    }
    if (a.name.toLowerCase() > b.name.toLowerCase()){
        return 1;
    }
    return 0;
  }

function prepare_benchmarks() {
    let bm_selection = document.getElementById("bm_selection");
    bm_selection.innerHTML = "";
    $.ajax('/fetch_benchmarks')
        .done(function (data) {
            let benchmarks = data.results;
            for (let index = 0; index < benchmarks.length; ++index) {
                bm_selection.innerHTML += "<option>" + benchmarks[index].docker_name + "</option>\n";
            }
            if (benchmarks.length === 0) {
                BENCHMARKS_EMPTY = true;
                document.getElementById("submit_button").setAttribute("disabled", "true");
            }
        })
}

function prepare_page() {
    document.getElementById("result_file").value = "";
    document.getElementById("custom_tag").value = "";
    document.getElementById('add_tag_button').setAttribute("disabled", "true");
    if (false !== document.getElementById("agreed_license").checked) {
        document.getElementById("agreed_license").click();
    }
    if (false !== document.getElementById("custom_site").checked) {
        document.getElementById("custom_site").click();
    }
    prepare_sites();
    prepare_tags();
    prepare_benchmarks();
}

window.onload = prepare_page;

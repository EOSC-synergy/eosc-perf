"use strict";

/**
 * String comparison helper using toLowerCase()
 * @param a first string
 * @param b second stringf
 * @returns {number} -1 if a < , 1 if a > b, 0 if a == b
 */
function compare(a, b) {
    if (a.name.toLowerCase() < b.name.toLowerCase()){
        return -1;
    }
    if (a.name.toLowerCase() > b.name.toLowerCase()){
        return 1;
    }
    return 0;
}

class ResultUpload {
    /**
     * Initialize result upload page
     */
    constructor() {
        this.agreedToLicense = false;
        this.noSites = false;
        this.customSite = false;
        this.benchmarksEmpty = false;

        let form = $('#form');
        form.submit(function (e) {
            let old_html = "";
            let selection = document.getElementById('site_selection');
            if (!this.customSite) {
                old_html = selection.options[selection.selectedIndex].innerHTML;
                selection.options[selection.selectedIndex].innerHTML = selection.options[selection.selectedIndex].id;
            }
            let formData = new FormData(this);
            upload_page.append_form_data(formData);
            submit_form(form, formData,
                function (data, textStatus) {
                    // display success message and reset page
                    display_message('Submission successful');
                    upload_page.reset_page();
                },
                function (data) {
                    window.location.href = data.responseJSON.redirect;
                });
            if (!this.customSite) {
                selection.options[selection.selectedIndex].innerHTML = old_html;
            }
            return false;
        });

        this.sites_data = new Map();

        this.siteSelection = document.getElementById("site_selection");
        this.siteSelection.addEventListener("change", function() {
            upload_page.on_site_select();
        });

        this.customSiteNameInput = document.getElementById("site_name");
        this.customSiteAddressInput = document.getElementById("site_address");
        this.customSiteDescriptionInput = document.getElementById("site_description");

        this.customFlavorDescriptionInput = document.getElementById("siteFlavorCustom");

        this.flavorInput = document.getElementById("siteFlavor");
        this.flavorInput.addEventListener("change", function() {
            upload_page.on_flavor_select();
        });

        this.submitButton = document.getElementById("submit_button");
        this.customTagInput = document.getElementById("custom_tag");

        this.reset_page();

        this.fetch_sites();
        this.fetch_tags();
        this.fetch_benchmarks();
    }

    /**
     * Callback for site option selection
     */
    on_site_select() {
        if (this.siteSelection.value === undefined || this.siteSelection.value.length === 0) {
            return;
        }

        clear_element_children(this.flavorInput);
        for (let flavor of this.sites_data.get(this.siteSelection.value).flavors) {
            let option = document.createElement("option");
            option.value = flavor.uuid;
            option.textContent = flavor.name;
            this.flavorInput.appendChild(option);
        }
    }

    /**
     * Callback for flavor option selection
     */
    on_flavor_select() {
        /*
        // not implemented yet
        if (this.flavorInput.value === "New...") {
            this.customFlavorDescriptionInput.classList.remove("d-none");
        }
        else {
            this.customFlavorDescriptionInput.classList.add("d-none");
        }
        */
    }

    /**
     * Callback for custom site checkbox
     * @param checkbox checkbox element
     */
    site_checkbox_click(checkbox) {
        this.customSite = checkbox.checked;
        if (this.customSite) {
            this.customSiteNameInput.disabled = false;
            this.customSiteAddressInput.disabled = false;
            this.customSiteDescriptionInput.disabled = false;
            this.siteSelection.disabled = true;
            this.flavorInput.disabled = true;
            if (!this.benchmarksEmpty && this.agreedToLicense) {
                this.submitButton.disabled = false;
            }
        }
        else {
            this.customSiteNameInput.disabled = true;
            this.customSiteNameInput.value = '';
            this.customSiteAddressInput.disabled = true;
            this.customSiteAddressInput.value = '';
            this.customSiteDescriptionInput.disabled = true;
            this.customSiteDescriptionInput.value = '';
            this.siteSelection.disabled = false;
            this.flavorInput.disabled = false;
            if (this.noSites) {
                this.submitButton.disabled = true;
            }
        }
    }

    /**
     * Callback for license checkbox
     * @param checkbox checkbox element
     */
    license_checkbox_click(checkbox) {
        this.agreedToLicense = checkbox.checked;
        if (this.agreedToLicense && (!this.noSites || this.customSite) && !this.benchmarksEmpty) {
            this.submitButton.removeAttribute("disabled");
        } else {
            this.submitButton.setAttribute("disabled", "true");
        }
    }

    /**
     * Display the result submission license to the user
     */
    show_license() {
        const license = document.getElementById("license").getAttribute("value");
        display_message(license, "License", true);
    }

    /**
     * Add extra non-form data to result submission form
     * @param formData form data
     */
    append_form_data(formData) {
        formData.append("custom_site", this.customSite);
        if (this.customSite) {
            formData.append("new_site_name", this.customSiteNameInput.value);
            formData.append("new_site_address", this.customSiteAddressInput.value);
            formData.append("new_site_description", this.customSiteDescriptionInput.value);
        }
    }

    /**
     * Callback for custom tag text box
     */
    stopped_typing_tag_field() {
        // only allow add tag button if length > 0
        document.getElementById('add_tag_button').disabled = this.customTagInput.value.trim().length <= 0;
    }

    /**
     * Submit a new tag
     */
    add_tag() {
        let tag = this.customTagInput.value.trim();
        submit_json('/upload_tag', {
                new_tag: tag
            },
            function (data, textStatus) {
                // reset tag field and reload tags
                upload_page.customTagInput.value = '';
                upload_page.fetch_tags();
            },
            function (data) {
                window.location.href = data.responseJSON.redirect;
            }
        );
    }

    /**
     * Fill obtained sites into the user form
     * @param data server response
     */
    fill_sites(data) {
        let sites = data.results;

        this.sites_data.clear();
        for (let site of sites) {
            let siteHumanName = site.name;
            let siteName = site.identifier;

            let option = document.createElement("option");
            option.id = siteName;
            option.value = siteName;
            option.textContent = siteHumanName;
            this.siteSelection.appendChild(option);

            this.sites_data.set(siteName, site);
        }
        if (sites.length === 0) {
            this.noSites = true;
            this.submitButton.disabled = true;
        }
        else {
            this.siteSelection.selectedIndex = 0;
        }

        this.on_site_select();
    }

    /**
     * Fetch the sites and their data from backend
     */
    fetch_sites() {
        clear_element_children(this.siteSelection);
        $.ajax('/fetch_sites')
            .done(function (data) {
                upload_page.fill_sites(data);
            });
    }

    /**
     * Fetch a list of tags from backend
     */
    fetch_tags() {
        let tagSelection = document.getElementById("tag_selection");
        $.ajax('/fetch_tags')
            .done(function (data) {
                clear_element_children(tagSelection);
                data.results.sort(compare);
                for (const tag of data.results) {
                    let option = document.createElement("option");
                    option.textContent = tag.name;
                    tagSelection.appendChild(option);
                }
                if (data.results.length === 0) {
                    let option = document.createElement("option");
                    option.textContent = "No tags found";
                    option.disabled = true;
                    tagSelection.appendChild(option);
                }
            });
    }

    /**
     * Fetch a list of benchmarks from backend
     */
    fetch_benchmarks() {
        let benchmarkSelection = document.getElementById("bm_selection");
        clear_element_children(benchmarkSelection);
        $.ajax('/fetch_benchmarks')
            .done(function (data) {
                let benchmarks = data.results;
                for (const benchmark of benchmarks) {
                    let option = document.createElement("option");
                    option.textContent = benchmark.docker_name;
                    benchmarkSelection.appendChild(option);
                }
                if (benchmarks.length === 0) {
                    this.benchmarksEmpty = true;
                    this.submitButton.disabled = true;
                }
            })
    }

    /**
     * Reset some fields to empty values to prevent accidentally submitting duplicate data
     */
    reset_page() {
        document.getElementById("result_file").value = '';
        this.customTagInput.value = '';
        document.getElementById('add_tag_button').setAttribute("disabled", "true");
        if (false !== document.getElementById("agreed_license").checked) {
            document.getElementById("agreed_license").click();
        }
        if (false !== document.getElementById("custom_site").checked) {
            document.getElementById("custom_site").click();
        }
    }
}

let upload_page = null;

window.addEventListener("load", function () {
    upload_page = new ResultUpload();
});

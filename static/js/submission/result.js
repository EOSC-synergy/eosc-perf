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

class MultiSelect {
    constructor(listGroupUl, possibleValues) {
        this.container = listGroupUl;
        this.values = Array.from(possibleValues);
        this.selected_values = new Set();

        // cleanup possible previous elements
        clear_element_children(listGroupUl);

        // populate listgroup
        let self = this;
        for (const value of self.values) {
            let option = document.createElement("li");
            option.classList.add("list-group-item");
            option.textContent = value;
            option.onclick = function() {
                if (option.classList.contains("active")) {
                    self._unselect_value(value);
                    option.classList.remove("active");
                }
                else {
                    self._select_value(value);
                    option.classList.add("active");
                }
            }
            listGroupUl.appendChild(option);
        }
        // add warning if no values available
        if (this.values.length === 0) {
            let noValuesInfo = document.createElement("div");
            noValuesInfo.textContent = "No tags found";
            noValuesInfo.disabled = true;
            listGroupUl.appendChild(noValuesInfo);
        }
    }

    _select_value(value) {
        this.selected_values.add(value);
    }
    _unselect_value(value) {
        this.selected_values.delete(value);
    }

    get_selected_values() {
        return Array.from(this.selected_values);
    }
}

class ResultUpload {
    /**
     * Initialize result upload page
     */
    constructor() {
        this.noSites = false;
        this.customSite = false;
        this.benchmarksEmpty = false;

        let self = this;

        let form = $('#form');
        form.submit(function (e) {
            // use FormData to transfer files for now
            submit_form(form, self._make_form_data(),
                function (data, textStatus) {
                    // display success message and reset page
                    display_message('Submission successful');
                    self.reset_page();
                });
            return false;
        });

        this.sites_data = new Map();

        this.licenseAgreementCheckbox = document.getElementById("agreed_license");
        this.licenseAgreementCheckbox.onchange = function() {
            self.agreedToLicense = self.licenseAgreementCheckbox.checked;
            self._check_submit_conditions();
        };
        this.agreedToLicense = this.licenseAgreementCheckbox.value === "true";


        this.fileSelection = document.getElementById("result_file");
        this.fileSelection.onchange = function() {
            self._check_submit_conditions();
        }

        this.benchmarkSelection = document.getElementById("bm_selection");

        this.siteSelection = document.getElementById("site_selection");
        this.siteSelection.addEventListener("change", function() {
            self.on_site_select();
        });

        this.customSiteInfoDiv = document.getElementById("customSiteInfo");
        this.customSiteNameInput = document.getElementById("site_name");
        this.customSiteNameInput.onkeyup = function() {
            self._check_submit_conditions();
        };
        this.customSiteAddressInput = document.getElementById("site_address");
        this.customSiteDescriptionInput = document.getElementById("site_description");
        this.customSiteFlavorInput = document.getElementById("customSiteFlavor");

        this.customFlavorDescriptionInput = document.getElementById("siteFlavorCustom");

        this.flavorSelectionDiv = document.getElementById("siteFlavorDiv");
        this.flavorSelection = document.getElementById("siteFlavor");
        this.flavorSelection.addEventListener("change", function() {
            self.on_flavor_select();
        });

        this.tagMultiselect = new MultiSelect(document.getElementById("tagSelection"), []);

        this.submitButton = document.getElementById("submit_button");
        this.customTagInput = document.getElementById("custom_tag");

        document.getElementById("tagSubmitButton").onclick = function() {
            self.submit_new_tag();
        };

        this.reset_page();

        this.fetch_sites();
        this.fetch_tags();
        this.fetch_benchmarks();
    }

    _check_submit_conditions() {
        if (this.agreedToLicense
            && !this.benchmarksEmpty
            && this.fileSelection.value.length > 4) {
            if (this.noSites && !this.customSite) {
                this.submitButton.disabled = true;
            }
            else if (this.customSite && this.customSiteNameInput.value.length === 0) {
                this.submitButton.disabled = true;
            }
            else {
                this.submitButton.disabled = false;
            }
        }
        else {
            this.submitButton.disabled = true;
        }
    }

    /**
     * Callback for site option selection
     */
    on_site_select() {
        if (this.siteSelection.value === undefined) {
            this.submitButton.disabled = true;
            return;
        }

        // custom site
        if (this.siteSelection.value.length === 0) {
            this.flavorSelectionDiv.classList.add("d-none");
            this.customSiteInfoDiv.classList.remove("d-none");
            this._set_custom_site_mode(true);
        }
        else {
            this.flavorSelectionDiv.classList.remove("d-none");
            this.customSiteInfoDiv.classList.add("d-none");
            this._set_custom_site_mode(false);
            clear_element_children(this.flavorSelection);
            for (let flavor of this.sites_data.get(this.siteSelection.value).flavors) {
                let option = document.createElement("option");
                option.value = flavor.uuid;
                option.textContent = flavor.name;
                this.flavorSelection.appendChild(option);
            }
        }
        this._check_submit_conditions();
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
     * Helper to set whether we're using a custom site
     * @param value whether we are creating a custom site or not
     */
    _set_custom_site_mode(value) {
        this.customSite = value;
        if (this.customSite) {
            this.customSiteNameInput.disabled = false;
            this.customSiteAddressInput.disabled = false;
            this.customSiteDescriptionInput.disabled = false;
            this.customSiteFlavorInput.disabled = false;
            this.flavorSelection.disabled = true;
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
            this.customSiteFlavorInput.disabled = true;
            this.customSiteFlavorInput.value = '';
            this.flavorSelection.disabled = false;
            if (this.noSites) {
                this.submitButton.disabled = true;
            }
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
     * Create FormData from scratch, fill in fields
     *
     * This is *not* based off the actual form to avoid values accidentally being added.
     */
    _make_form_data() {
        let formData = new FormData();
        formData.append('resultData', $('input[type=file]')[0].files[0], 'data.json');
        formData.append('benchmark', this.benchmarkSelection.value);
        formData.append('siteIdentifier', this.siteSelection.value);
        if (this.customSite) {
            formData.append("customSiteIdentifier", this.customSiteNameInput.value);
            formData.append("customSiteAddress", this.customSiteAddressInput.value);
            formData.append("customSiteDescription", this.customSiteDescriptionInput.value);
            formData.append("customSiteFlavor", this.customSiteFlavorInput.value);
        }
        else {
            formData.append("siteFlavor", this.flavorSelection.value);
        }
        for (const tag of this.tagMultiselect.get_selected_values()) {
            formData.append("tags", tag);
        }
        return formData;
    }

    /**
     * Callback for custom tag text box
     */
    stopped_typing_tag_field() {
        // only allow add tag button if length > 0
        document.getElementById('tagSubmitButton').disabled = this.customTagInput.value.trim().length <= 0;
    }

    /**
     * Submit a new tag
     */
    submit_new_tag() {
        let tag = this.customTagInput.value.trim();
        let self = this;
        submit_json('/upload_tag', {
                new_tag: tag
            },
            function (data, textStatus) {
                // reset tag field and reload tags
                self.customTagInput.value = '';
                self.fetch_tags();
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

        // new-site option
        {
            let option = document.createElement("option");
            option.value = "";
            option.textContent = "New...";
            this.siteSelection.appendChild(option);
        }
        if (sites.length === 0) {
            this.noSites = true;
        }
        this.siteSelection.selectedIndex = 0;

        this.on_site_select();
    }

    /**
     * Fetch the sites and their data from backend
     */
    fetch_sites() {
        clear_element_children(this.siteSelection);
        let self = this;
        $.ajax('/fetch_sites')
            .done(function (data) {
                self.fill_sites(data);
            });
    }

    /**
     * Fetch a list of tags from backend
     */
    fetch_tags() {
        let self = this;
        $.ajax('/fetch_tags')
            .done(function (data) {
                data.results.sort(compare);

                self.tagMultiselect = new MultiSelect(document.getElementById("tagSelection"), data.results.map(meta => meta.name));
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
        document.getElementById('tagSubmitButton').disabled = true;
        if (this.licenseAgreementCheckbox.checked) {
            this.licenseAgreementCheckbox.click();
        }
    }
}

let upload_page = null;

window.addEventListener("load", function () {
    upload_page = new ResultUpload();
});

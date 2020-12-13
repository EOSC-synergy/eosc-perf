
/**
 * Clear all child elements of a given element.
 * @param element The element to remove all children from.
 * @private
 */
function _clear_children(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function _fill_list_item(item, data) {
    item.id = data.short_name;
    item.classList.add("list-group-item", "list-group-item-action", "flex-column", "align-items-start");

    let headingDiv = document.createElement("div");
    headingDiv.classList.add("d-flex","w-100", "justify-content-between");
    let heading = document.createElement("h5");
    heading.classList.add("mb-1");
    heading.textContent = data.name;
    headingDiv.appendChild(heading);
    let headingExtra = document.createElement("small");
    headingExtra.textContent = data.short_name;
    headingDiv.appendChild(headingExtra);
    item.appendChild(headingDiv);

    let descParagraph = document.createElement("p");
    descParagraph.classList.add("mb-1");
    descParagraph.textContent = data.description;
    item.appendChild(descParagraph);

    let addressSmall = document.createElement("small");
    addressSmall.textContent = data.address;
    item.appendChild(addressSmall);
}

class SiteEditor {
    constructor() {
        this.selectedSite = null;
        this.entries = new Map();

        this._poll_sites();
    }
    _poll_sites() {
        $.ajax('/fetch_sites').done(function (data) {
            site_editor._update_sites(data.results);
        });
    }
    _clear_sites() {
        let list = document.getElementById("siteListGroup");
        _clear_children(list);
        this.entries.clear();
    }

    _update_sites(sites) {
        this._clear_sites();
        let list = document.getElementById("siteListGroup");
        for (let siteData of sites) {
            let listItem = document.createElement("a");
            _fill_list_item(listItem, siteData);

            listItem.addEventListener("click", function(e) {
                e.preventDefault();
                site_editor.select_site(listItem.id);
            });

            list.appendChild(listItem);

            this.entries.set(siteData.short_name, siteData);
        }
    }

    select_site(siteId) {
        if (this.selectedSite != null) {
            document.getElementById(this.selectedSite).classList.remove("active");
        }
        this.selectedSite = siteId;
        let siteEntry = document.getElementById(siteId);
        siteEntry.classList.add("active");

        let entry = this.entries.get(siteId);

        document.getElementById("short_name").value = entry.short_name;
        document.getElementById("full_name").value = entry.name;
        document.getElementById("description").value = entry.description;
        document.getElementById("address").value = entry.address;

        document.getElementById("siteUpdateForm").classList.remove("d-none");
    }

    update_current_site_entry() {
        if (this.selectedSite == null) {
            return;
        }
        let data = this.entries.get(this.selectedSite);
        data.short_name = document.getElementById("short_name").value;
        data.name = document.getElementById("full_name").value;
        data.description = document.getElementById("description").value;
        data.address = document.getElementById("address").value;
        this.entries.set(this.selectedSite, data);
        let listItem = document.getElementById(this.selectedSite);
        _clear_children(listItem);
        _fill_list_item(listItem, data);
    }
}

//
let site_editor = null;

window.addEventListener("load", function () {
    site_editor = new SiteEditor();

    let form = $('#siteUpdateForm');
    form.submit(function (e) {
        document.getElementById("loading-icon").classList.remove("d-none");
        submit_form_json(form, form.serialize(),
            function (data, textStatus) {
                site_editor.update_current_site_entry();
                document.getElementById("loading-icon").classList.add("d-none");
            },
            function (data) {
                window.location.href = data.responseJSON.redirect;
            }
        );

        return false;
    });
});
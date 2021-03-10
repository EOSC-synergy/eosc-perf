
const NEW_FLAVOR_ID = "new_flavor";

function _fill_site_item(item, data) {
    item.id = data.identifier;
    item.classList.add("list-group-item", "list-group-item-action", "flex-column", "align-items-start");

    let headingDiv = document.createElement("div");
    headingDiv.classList.add("d-flex","w-100", "justify-content-between");
    let heading = document.createElement("h5");
    heading.classList.add("mb-1");
    heading.textContent = data.name;
    headingDiv.appendChild(heading);
    let headingExtra = document.createElement("small");
    headingExtra.textContent = data.identifier;
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

function _fill_flavor_item(item, data) {
    item.id = data.uuid;
    item.classList.add("list-group-item", "list-group-item-action", "flex-column", "align-items-start");

    // -- heading + update button
    let headingDiv = document.createElement("div");
    headingDiv.classList.add("d-flex","w-100", "justify-content-between");
    let heading = document.createElement("h5");
    heading.classList.add("mb-1");
    // --- heading text box
    let headingInputGroup = document.createElement("div");
    headingInputGroup.classList.add("input-group", "mb-3");
    let headingInput = document.createElement("input");
    headingInput.classList.add("form-control", "nameInput");
    headingInput.value = data.name;
    headingInput.readOnly = true;
    headingInput.name = "flavor_title";
    // --- heading update button
    let headingUpdateDiv = document.createElement("div");
    headingUpdateDiv.classList.add("input-group-append");
    let headingUpdateButton = document.createElement("button");
    headingUpdateButton.classList.add("btn", "btn-secondary", "updateButton");
    headingUpdateButton.disabled = true;
    let headingUpdateButtonText = document.createElement("i");
    headingUpdateButtonText.classList.add("bi", "bi-check");
    headingUpdateButton.appendChild(headingUpdateButtonText);
    headingUpdateDiv.appendChild(headingUpdateButton);
    // --- edit button
    let headingEditDiv = document.createElement("div");
    headingEditDiv.classList.add("input-group-append");
    let headingEditButton = document.createElement("button");
    headingEditButton.classList.add("btn", "btn-secondary", "editButton");
    let headingEditButtonText = document.createElement("i");
    headingEditButtonText.classList.add("bi", "bi-pencil-square");
    headingEditButton.appendChild(headingEditButtonText);
    headingEditDiv.appendChild(headingEditButton);

    headingInputGroup.appendChild(headingInput);
    headingInputGroup.appendChild(headingUpdateDiv);
    headingInputGroup.appendChild(headingEditDiv);
    heading.appendChild(headingInputGroup);
    headingDiv.appendChild(heading);
    item.appendChild(headingDiv);
    // -- description
    let descParagraph = document.createElement("p");
    descParagraph.classList.add("mb-1");
    let descInput = document.createElement("textarea");
    descInput.value = data.description;
    descInput.readOnly = true;
    descInput.classList.add("form-control", "descInput");
    descParagraph.appendChild(descInput);

    item.appendChild(descParagraph);
}

class SiteEditor {
    constructor() {
        this.selectedSite = null;
        this.selectedFlavor = null;
        this.entries = new Map();

        document.getElementById("addFlavor").addEventListener("click", function(e) {
            e.preventDefault();
            site_editor.new_flavor();
        });
        this._poll_sites();
    }

    _poll_sites() {
        $.ajax('/fetch_sites').done(function (data) {
            site_editor._update_sites(data.results);
        });
    }

    _clear_sites() {
        let list = document.getElementById("siteListGroup");
        clear_element_children(list);
        this.entries.clear();
    }

    _update_sites(sites) {
        this._clear_sites();
        let list = document.getElementById("siteListGroup");
        for (let siteData of sites) {
            let listItem = document.createElement("a");
            _fill_site_item(listItem, siteData);

            listItem.addEventListener("click", function(e) {
                e.preventDefault();
                site_editor.select_site(listItem.id);
            });

            list.appendChild(listItem);

            this.entries.set(siteData.identifier, siteData);
        }
    }

    _fill_flavors(flavors) {
        for (let flavor of flavors) {
            this.add_flavor(flavor);
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

        document.getElementById("identifier").value = entry.identifier;
        document.getElementById("full_name").value = entry.name;
        document.getElementById("description").value = entry.description;
        document.getElementById("address").value = entry.address;

        clear_element_children(document.getElementById("flavorListGroup"));
        this._fill_flavors(entry.flavors);

        document.getElementById("siteUpdateForm").classList.remove("d-none");
    }

    enable_flavor_edit(uuid) {
        if (this.selectedFlavor === uuid) {
            return;
        }
        this.disable_flavor_edit();
        this.selectedFlavor = uuid;
        let flavorEntry = document.getElementById(uuid);
        let button = flavorEntry.querySelector('.updateButton');
        button.disabled = false;
        button.addEventListener("onclick", function (e) {
            site_editor.submit_flavor_edit(uuid);
        });
        flavorEntry.querySelector('.nameInput').readOnly = false;
        flavorEntry.querySelector('.descInput').readOnly = false;
    }

    disable_flavor_edit() {
        if (this.selectedFlavor != null) {
            let element = document.getElementById(this.selectedFlavor);
            if (element.id === NEW_FLAVOR_ID) {
                this.remove_flavor(NEW_FLAVOR_ID);
            }
            else {
                element.querySelector('.updateButton').disabled = true;
                element.querySelector('.nameInput').readOnly = true;
                element.querySelector('.descInput').readOnly = true;
                if (element.querySelector('.alert') !== null) {
                    element.removeChild(element.querySelector('.alert'));
                }
            }
        }
        this.selectedFlavor = null;
    }

    new_flavor() {
        if (document.getElementById(NEW_FLAVOR_ID) !== null) {
            return;
        }
        this.add_flavor({"name": "new", "description": "", "uuid": NEW_FLAVOR_ID});
        this.disable_flavor_edit();
        this.enable_flavor_edit(NEW_FLAVOR_ID);
    }

    add_flavor(data) {
        let list = document.getElementById("flavorListGroup");
        let listItem = document.createElement("a");
        _fill_flavor_item(listItem, data);

        listItem.querySelector(".editButton").addEventListener("click", function(e) {
            e.preventDefault();
            site_editor.enable_flavor_edit(listItem.id);
        });
        listItem.querySelector(".updateButton").addEventListener("click", function(e) {
            e.preventDefault();
            site_editor.submit_flavor_edit(data.uuid);
        });

        list.appendChild(listItem);
    }

    remove_flavor(uuid) {
        let flavor = document.getElementById(uuid);
        flavor.parentElement.removeChild(flavor);
    }

    display_flavor_update_response(uuid, alertClass, message) {
        let flavorEntry = document.getElementById(uuid);
        let alertMessage = document.createElement("div");
        alertMessage.classList.add("alert", alertClass);
        alertMessage.role = "alert";
        alertMessage.textContent = message;
        flavorEntry.appendChild(alertMessage);
    }

    submit_flavor_edit(uuid) {
        let flavor_entry = document.getElementById(uuid);
        let name = flavor_entry.querySelector('.nameInput').value;
        let description = flavor_entry.querySelector('.descInput').value;
        let update = {
            "name": name,
            "description": description,
            "uuid": uuid
        };
        if (uuid === NEW_FLAVOR_ID) {
            update.site = document.getElementById("identifier").value;
        }
        $.ajax({
            type: "POST",
            url: "/update/flavor",
            data: JSON.stringify(update),
            contentType: "application/json",
            dataType: "json",
            success: function (data, status, xhr) {
                site_editor.disable_flavor_edit();
                if (uuid === NEW_FLAVOR_ID) {
                    //site_editor.remove_flavor(NEW_FLAVOR_ID);
                    site_editor.add_flavor(
                        {"name": update.name, "description": update.description, "uuid": data.uuid});
                    uuid = data.uuid;
                }
            },
            error: function (data, status, xhr) {
                site_editor.display_flavor_update_response(uuid, "alert-warning", "Error: " +
                    data.error);
            }
        });
    }

    update_current_site_entry() {
        if (this.selectedSite == null) {
            return;
        }
        let data = this.entries.get(this.selectedSite);
        data.identifier = document.getElementById("identifier").value;
        data.name = document.getElementById("full_name").value;
        data.description = document.getElementById("description").value;
        data.address = document.getElementById("address").value;
        this.entries.set(this.selectedSite, data);
        let listItem = document.getElementById(this.selectedSite);
        clear_element_children(listItem);
        _fill_site_item(listItem, data);
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
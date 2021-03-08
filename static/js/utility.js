
class Modal {
    /**
     * Build a bootstrap modal
     * @param title title text
     * @param body body div
     * @param footer footer div (should contain close button with data-dismiss="modal")
     */
    constructor(title, body, footer) {
        this.modal = document.createElement("div");
        this.modal.classList.add("modal", "fade");
        this.modal.tabIndex = -1;
        this.modal.setAttribute("role", "dialog");
        {
            let modalDialog = document.createElement("div");
            modalDialog.classList.add("modal-dialog");
            modalDialog.setAttribute("role", "document");
            {
                let modalContent = document.createElement("div");
                modalContent.classList.add("modal-content");

                {
                    let modalHeader = document.createElement("div");
                    modalHeader.classList.add("modal-header");
                    {
                        this.modalTitle = document.createElement("div");
                        this.modalTitle.classList.add("modal-title");
                        this.modalTitle.textContent = title;
                        modalHeader.appendChild(this.modalTitle);

                        let closeButton = document.createElement("button");
                        closeButton.type = "button";
                        closeButton.classList.add("close");
                        closeButton.dataset.dismiss = "modal";
                        closeButton.setAttribute("aria-label", "Close");
                        {
                            let closeSymbol = document.createElement("span");
                            closeSymbol.setAttribute("aria-hidden", "true");
                            closeSymbol.textContent = "×"; // &times; / multiplication symbol
                            closeButton.appendChild(closeSymbol);
                        }
                        modalHeader.appendChild(closeButton);
                    }
                    modalContent.appendChild(modalHeader);

                    this.modalBody = document.createElement("div");
                    this.modalBody.classList.add("modal-body");
                    this.modalBody.appendChild(body);
                    modalContent.appendChild(this.modalBody);

                    this.modalFooter = document.createElement("div");
                    this.modalFooter.classList.add("modal-footer");
                    this.modalFooter.appendChild(footer);
                    modalContent.appendChild(this.modalFooter);
                }
                modalDialog.appendChild(modalContent);
            }
            this.modal.appendChild(modalDialog);
        }
    }

    display() {
        $(this.modal).modal('show');
    }

    cleanup() {
        //$(this.modal).modal('dispose');
        this.modal.remove();
    }
}

/**
 * Display a message.
 * @param message The message to display.
 * @param title An optional title.
 * @param html Whether the message should be treated as HTML text.
 */
function display_message(message, title = null, html = false) {
    let contentDiv = document.createElement("div");
    if (html) {
        contentDiv.innerHTML = message;
    }
    else {
        contentDiv.textContent = message;
    }
    let footer = document.createElement("div");
    let closeButton = document.createElement("button");
    closeButton.type = "button";
    closeButton.classList.add("btn", "btn-secondary");
    closeButton.dataset.dismiss = "modal";
    closeButton.textContent = "Close";
    footer.appendChild(closeButton);
    let modal = new Modal(title === null ? '' : title, contentDiv, footer);
    closeButton.onclick = function(e){ modal.cleanup() };

    modal.display();
}

/**
 * Send a form to the server by AJAX.
 * @param form the HTML form with method='POST or GET' and action='/endpoint' attributes
 * @param formData the data structure to send
 * @param on_success callback taking (data, textStatus)
 * @param on_fail callback taking (data) in case of errors
 */
function submit_form(form, formData, on_success, on_fail) {
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: formData,
        processData: false,
        contentType: false,
        success: on_success,
        error: on_fail
    });
}

/**
 * Send a form to the server as JSON by AJAX.
 * @param form the HTML form with method='POST or GET' and action='/endpoint' attributes
 * @param data the data structure to send
 * @param success callback taking (data, textStatus)
 * @param fail callback taking (data) in case of errors
 */
function submit_form_json(form, data, success, fail) {
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: data,
        dataType: "json",
        success: success,
        error: fail
    });
}

/**
 * Send JSON data to the server by AJAX.
 * @param form the HTML form with method='POST or GET' and action='/endpoint' attributes
 * @param data the data structure to send
 * @param success callback taking (data, textStatus)
 * @param fail callback taking (data) in case of errors
 */
function submit_json(url, data, success, fail) {
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        dataType: "json",
        success: success,
        error: fail
    });
}

/**
 * Clear all child elements of a given element.
 * @param element The element to remove all children from.
 */
function clear_element_children(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

/**
 * Helper to open link in new tab
 *
 * See https://stackoverflow.com/a/28374344.
 *
 * @param href page to open
 */
function open_tab(href) {
    Object.assign(document.createElement('a'),
        {
            target: '_blank',
            href: href,
        }).click();
}

function login() {
    // store where we were
    window.sessionStorage.setItem('after_auth_redirect_url', window.location);
    // go to login page
    window.location.href = '/login';
}
function loginThenGoTo(destination) {
    // store where we're going
    window.sessionStorage.setItem('after_auth_redirect_url', destination);
    // go to login page
    window.location.href = '/login';
}

function logout() {
    // store where we were
    window.sessionStorage.setItem('after_auth_redirect_url', window.location);
    // go to logout page
    window.location.href = '/logout';
}

/**
 * Helpers for the hardcoded data from flask
 */
function isLoggedIn() {
    return logged_in;
}
function isAdmin() {
    return admin;
}
function isDebug() {
    return debug;
}
function getUsername() {
    return user_name;
}
function getSupportEmail() {
    return support_email;
}
function getInfrastructureManager() {
    return im_link;
}

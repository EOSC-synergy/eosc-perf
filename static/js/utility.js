/**
 * Display a message.
 * @param message The message to display.
 */
function display_message(message) {
    document.getElementById('overlay-text').innerHTML = message;
    document.getElementById('overlay').style.display = 'block';
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
 * Send a form to the server by AJAX.
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
 * Clear all child elements of a given element.
 * @param element The element to remove all children from.
 * @private
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

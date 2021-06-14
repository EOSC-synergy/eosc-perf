/**
 * This script is loaded by templates/redirect_return.jinja2.html.
 */

window.addEventListener("load", function () {
    const url = window.sessionStorage.getItem('after_auth_redirect_url');
    if (url != null) {
        window.sessionStorage.removeItem('after_auth_redirect_url');
        window.location.replace(url);
    }
});

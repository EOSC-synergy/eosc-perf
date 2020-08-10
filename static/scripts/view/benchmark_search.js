$(function () {
    form = $('#form');
    form.submit(function (e) {
        alert('Search button clicked.');
        return false;
    });
});

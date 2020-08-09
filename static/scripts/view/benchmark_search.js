$(function () {
    form = $('#form');
    form.submit(function (e) {
        consolelog("test")
        return true;
    });
});

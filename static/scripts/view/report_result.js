$(function () {
    let form = $('#form');
    form.submit(function (e) {
        submit_form(form, form.serialize(),
            function (data, textStatus) {
                // display success message and disable form
                display_message('Submission successful');
                $('#form input[type="submit"]').prop("disabled", true);
            },
            function (data) {
                window.location.href = data.responseJSON.redirect;
            });

        return false;
    });
});

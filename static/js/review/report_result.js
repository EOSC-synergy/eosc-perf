window.addEventListener("load", function () {
    let form = $('#form');
    form.submit(function (e) {
        submit_form_json(form, form.serialize(),
            function (data, textStatus) {
                // display success message and disable form
                display_message('Submission successful');
                $('#form input[type="submit"]').prop("disabled", true);
            });

        return false;
    });

    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightBlock(block);
    });
});

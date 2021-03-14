$(function () {
    let form = $('#form');
    form.submit(function (e) {
        let data = {
            'uuid': form.find('input[name="uuid"]').val(),
            'action': e.originalEvent.submitter.name
        };
        submit_form_json(form, data,
            function (data, textStatus) {
                // display success message and disable form
                display_message('Verdict submitted');
                $('#form input[type="submit"]').prop("disabled", true);
            });

        return false;
    });

    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightBlock(block);
    });
});

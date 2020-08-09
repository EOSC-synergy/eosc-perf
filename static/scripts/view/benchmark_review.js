$(function () {
    form = $('#form');
    form.submit(function (e) {
        data = {};
        data['uuid'] = form.find('input[name="uuid"]').val();
        data['action'] = e.originalEvent.submitter.name;
        console.log(data);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: data,
            dataType: "json",
            success: function (data, textStatus) {
                // display success message and disable form
                $('#overlay-text').text('Review successful');
                $('#overlay').show();
                $('#form input[type="submit"]').prop("disabled", true);
            },
            error: function (data) {
                window.location.href = data.responseJSON.redirect;
            }
        });

        return false;
    });
});

$(function () {
    form = $('#form');
    form.submit(function (e) {
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            dataType: "json",
            success: function (data, textStatus) {
                // display success message and disable form
                $('#overlay-text').text('Submission successful');
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

function stopped_typing(){
    if(document.getElementById("docker_name").value.trim().length > 0) {
        document.getElementById("submit").removeAttribute("disabled");
    } else {
        document.getElementById("submit").setAttribute("disabled", true);
    }
}
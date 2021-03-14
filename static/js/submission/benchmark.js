$(function () {
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
});

function stopped_typing(){
    if(document.getElementById("docker_name").value.trim().length > 0) {
        document.getElementById("submit").removeAttribute("disabled");
    } else {
        document.getElementById("submit").setAttribute("disabled", "true");
    }
}
function checkPasswords() {
    if (document.getElementById('id_change_password')) {
        checkbox = document.getElementById('id_change_password');
        if (checkbox.checked) {
            document.getElementById('passwordChange').style.display = "block";
        } else {
            document.getElementById('passwordChange').style.display = "none";
        }
    }
}

$(document).ready(function () {
    checkPasswords();

    // Check if the user has confirmed the Terms and Conditions clause.
    $('#terms').change(function () {
        if (this.checked) {
            $('#submit-button').prop('disabled', false);
        }
        else {
            $('#submit-button').prop('disabled', true);
        }
    });
});

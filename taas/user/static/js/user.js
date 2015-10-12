$(function () {
    $(".tab-menu li").click(function () {
        $(".tab-menu li").removeClass('selected');
        $(this).addClass('selected');
    });
});

function checkPasswords() {
    checkbox = document.getElementById('id_change_password');
    if (checkbox.checked) {
        document.getElementById('passwordChange').style.display = "block";
    } else {
        document.getElementById('passwordChange').style.display = "none";
    }
}
window.onload = checkPasswords;
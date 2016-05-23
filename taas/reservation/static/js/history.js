swal.setDefaults({confirmButtonColor: '#ffa31a'});

function remove_reservation(reservation_id) {
    swal({
        title: title,
        text: removeMessage,
        type: "warning",
        showCancelButton: true,
        confirmButtonText: "OK",
        cancelButtonText: cancelMessage,
        closeOnConfirm: true
    }, function () {
        swal("Deleted!", "Your reservation has been deleted.", "success");
        jQuery.post('/reservation/remove/', {id: reservation_id},
            function () {
                location.reload()
            }, "json")
    });
}

function update_reservation(reservation_id) {
    swal({
        title: title,
        text: updateMessage,
        type: "warning",
        showCancelButton: true,
        confirmButtonText: "OK",
        cancelButtonText: cancelMessage,
        closeOnConfirm: true
    }, function () {
        window.location.replace("/reservation/update/" + reservation_id);
    });
}

$(document).ready(function () {
    // Check if the user has confirmed the Terms and Conditions clause.
    $('#terms').change(function () {
        if (this.checked) {
            console.log("IT works!!");
            $('.submit-button').attr("disabled", false);
        }
        else {
            $('.submit-button').prop('disabled', true);
        }
    });
});
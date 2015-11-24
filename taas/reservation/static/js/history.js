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
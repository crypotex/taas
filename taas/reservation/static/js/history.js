swal.setDefaults({confirmButtonColor: '#ffa31a'});

function remove_reservation(reservation_id) {
    swal({
        title: "Are you sure?",
        text: removeMessage,
        type: "warning",
        showCancelButton: true,
        confirmButtonText: "OK",
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
        title: "Are you sure?",
        text: updateMessage,
        type: "warning",
        showCancelButton: true,
        confirmButtonText: "OK",
        closeOnConfirm: true
    }, function () {
        window.location.replace("/reservation/update/" + reservation_id);
    });
}
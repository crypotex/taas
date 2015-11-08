function remove_reservation(reservation_id) {
    jQuery.post('/reservation/remove/', {id: reservation_id},
        function () {
            location.reload()
        }, "json")
}
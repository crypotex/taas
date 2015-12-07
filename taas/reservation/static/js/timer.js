var expireDate = null;

swal.setDefaults({confirmButtonColor: '#ffa31a'});

function setExpireDate() {
    jQuery.ajax({
        url: '/reservation/expire/',
        success: function (data) {
            if (data['response']) {
                expireDate = new Date();
                expireDate.setMinutes(expireDate.getMinutes() + parseInt(data['response'].split(":")[0]));
                expireDate.setSeconds(expireDate.getSeconds() + parseInt(data['response'].split(":")[1]));
                startTimer(expireDate);
            }
        },
        async: false,
        cache: false
    });
}

function startTimer(expireDate) {
    document.getElementById('timerMessage').style.display = 'block';
    $('#timer').countdown(expireDate, function (event) {
        $(this).html(event.strftime('%M:%S'));
    }).on('finish.countdown', function () {
        stopTimer();
        removeReservationsOnExpire();
        swal({title: warningMessage, text: expireMessage, type: "warning", confirmButtonText: "OK"});
    });
}

function stopTimer() {
    document.getElementById('timerMessage').style.display = 'none';
    $('#timer').countdown('stop');
}

function removeReservationsOnExpire() {
    jQuery.post('/reservation/remove/all/').done(
        function () {
            stopTimer();
            swal({title: warningMessage, text: expireMessage, type: "warning", confirmButtonText: "OK"});
        }
    )
}

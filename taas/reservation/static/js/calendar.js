var canSelect;
var timeError;
var expireMessage;
var expireDate = null;
var warningMessage;
var fieldA;
var fieldB;
var fieldC;

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
        disableSubmition();
        expireDate = null;
        swal({title: warningMessage, text: expireMessage, type: "warning", confirmButtonText: "OK"});
    });
}


function stopTimer() {
    document.getElementById('timerMessage').style.display = 'none';
    $('#timer').countdown('stop');
}

function disableSubmition() {
    document.getElementById('submitBookings').style.display = 'none';
}

function enableSubmition() {
    document.getElementById('submitBookings').style.display = 'block';
}

function removeReservationsOnExpire() {
    jQuery.post('/reservation/remove/all/').done(
        function () {
            $("#calendar").fullCalendar('refetchEvents');
        }
    )
}

function addReservation(start, end, ev) {
    var minutes = start.diff(moment(), 'minutes');
    if (minutes < 30) {
        swal({title: warningMessage, text: timeError, type: "warning", customClass: "alert-button"});
    } else {
        jQuery.post('reservation/add/',
            {
                start: start.zone('+0200').format('YYYY-MM-DD HH:mm'),
                end: end.zone('+0200').format('YYYY-MM-DD HH:mm'),
                field: ev.data.name
            }
        ).done(function () {
                $("#calendar").fullCalendar('refetchEvents');
                if (!expireDate) {
                    expireDate = moment().add(10, 'minutes').toDate();
                }
                startTimer(expireDate);
                enableSubmition();
            }
        );
    }
}

function deleteReservation(calEvent) {
    if (calEvent.color != "#b285e0") return;

    jQuery.post('/reservation/remove/',
        {
            id: calEvent.id
        },
        function (data) {
            if (!data.response) {
                disableSubmition();
                stopTimer();
                expireDate = null;
            }
        },
        "json"
    ).done(
        function () {
            $("#calendar").fullCalendar('refetchEvents');
        }
    )
}

$(document).ready(function () {
    $("#calendar").fullCalendar({
        header: {
            left: '',
            center: 'title',
            right: ''
        },
        resources: 'reservation/fields/',
        defaultView: 'resourceDay',
        allDaySlot: false,
        minTime: '08:00:00',
        maxTime: '22:00:00',
        aspectRatio: 0.0,
        theme: true,
        axisFormat: 'HH:mm',
        timeFormat: '',
        timezone: 'local',
        slotDuration: '01:00:00',
        selectable: canSelect,
        selectHelper: true,
        select: addReservation,
        events: '/reservation/all/',
        eventClick: deleteReservation
    });

    $('.fc-col0').tooltipster({
        theme: 'tooltipster-light',
        offsetX: -135,
        content: $(fieldA)
    });

    $('.fc-col1').tooltipster({
        theme: 'tooltipster-light',
        offsetX: -135,
        content: $(fieldB)
    });

    $('.fc-col2').tooltipster({
        theme: 'tooltipster-light',
        offsetX: -135,
        content: $(fieldC)
    });

    $('#datepicker').datepicker({
        inline: true,
        firstDay: 1,
        onSelect: function () {
            $('#calendar').fullCalendar('gotoDate', $('#datepicker').datepicker('getDate'));
        }
    });
});
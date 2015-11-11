var canSelect;
var timeError;
var expireMessage;
var expire_date = null;

swal.setDefaults({confirmButtonColor: '#ffa31a'});

function startTimer() {
    if (expire_date != null) {
        $('#timer').countdown(expire_date, function (event) {
            $(this).html(event.strftime('%M:%S'));
        }).on('finish.countdown', function () {
            removeReservationsOnExpire();
        });
    }
}

function getExpireDate() {
    jQuery.get('/reservation/expire/', function (date) {
        expire_date = new Date();
        expire_date.setMinutes(expire_date.getMinutes() + parseInt(date['response'].split(":")[0]));
        expire_date.setSeconds(expire_date.getSeconds() + parseInt(date['response'].split(":")[1]));
    }).done(function () {
        console.log("Date: " + expire_date);
        startTimer();
    });
}

function disableSubmition() {
    if (document.getElementById('submit')) {
        document.getElementById('submit').style.visibility = 'hidden';
    }
    document.getElementById('timerMessage').style.visibility = 'hidden';
    expire_date = null;
}

function enableSubmition() {
    if (document.getElementById('submit')) {
        document.getElementById('submit').style.visibility = 'visible';
    }
    document.getElementById('timerMessage').style.visibility = 'visible';
    startTimer();
}

function removeReservationsOnExpire() {
    jQuery.post('/reservation/remove/all/').done(
        function () {
            if ($('#calendar').length) {
                $("#calendar").fullCalendar('refetchEvents');
            }
            disableSubmition();
            swal({title: "Warning", text: expireMessage, type: "warning", confirmButtonText: "OK"});
        }
    )
}

function addReservation(start, end, ev) {
    var minutes = start.diff(moment(), 'minutes');
    if (minutes < 15) {
        swal({title: "Warning", text: timeError, type: "warning", customClass: "alert-button"});
    } else {
        jQuery.post('reservation/add/',
            {
                start: start.zone('+0200').format('YYYY-MM-DD HH:mm'),
                end: end.zone('+0200').format('YYYY-MM-DD HH:mm'),
                field: ev.data.name
            }
        ).done(function () {
                $("#calendar").fullCalendar('refetchEvents');
                getExpireDate();
                enableSubmition();
            }
        );

    }
}

function deleteReservation(calEvent) {
    if (calEvent.color != "#008000") return;

    jQuery.post('/reservation/remove/',
        {
            id: calEvent.id
        },
        function (data) {
            if (!data.response) {
                disableSubmition()
            }
        },
        "json"
    ).done(
        function () {
            $("#calendar").fullCalendar('refetchEvents');
        }
    )
}

function checkDate() {
    var now = new Date();
    var check_date = new Date(expire_date);
    if (check_date <= now) {
        removeReservationsOnExpire()
    }
}

$(document).ready(function () {
    if ($('#calendar').length) {
        $("#calendar").fullCalendar({
            header: false,
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
    }
    if ($('#datepicker').length) {
        $('#datepicker').datepicker({
            inline: true,
            minDate: 0,
            firstDay: 1,
            onSelect: function () {
                $('#calendar').fullCalendar('gotoDate', $('#datepicker').datepicker('getDate'));
            }
        });
    }
});
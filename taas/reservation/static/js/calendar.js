var canSelect;
var timeError;
var expireMessage;
var expire_date = null;

swal.setDefaults({ confirmButtonColor: '#ffa31a' });

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function startTimer() {
    if (expire_date == null) {
        expire_date = new Date();
        expire_date.setMinutes(expire_date.getMinutes() + 10);
    }
    $('#timer').countdown(expire_date, function (event) {
        $(this).html(event.strftime('%M:%S'));
    }).on('finish.countdown', function (event) {
        removeReservationsOnExpire()
    });
}

function disableSubmition() {
    document.getElementById('submit').style.visibility = 'hidden';
    document.getElementById('timerMessage').style.visibility = 'hidden';
    expire_date = null;
}

function enableSubmition() {
    document.getElementById('submit').style.visibility = 'visible';
    document.getElementById('timerMessage').style.visibility = 'visible';
    startTimer()
}

function removeReservationsOnExpire() {
    jQuery.post('reservation/remove/all/').done(
        function () {
            $("#calendar").fullCalendar('refetchEvents');
            disableSubmition();
            swal({title: "Warning", text: expireMessage, type: "warning", confirmButtonText: "OK"});
        }
    )
}

function addReservation(start, end, ev) {
    $(".fc-cell-overlay").removeClass("fc-cell-overlay");
    $(this).addClass('fc-cell-overlay');
    var check = new Date(start.toISOString());
    var now = new Date();
    var diff = Math.floor((Math.abs(now - check) / 1000) / 60);
    if (check < now || diff < 30) {
        swal({title: "Warning", text: timeError, type: "warning", customClass: "alert-button"});
    }
    else {
        jQuery.post('reservation/add/',
            {
                start: start.format(),
                end: end.format(),
                field: ev.data.name
            }
        ).done(function () {
                $("#calendar").fullCalendar('refetchEvents');
                enableSubmition()
            }
        )
    }
}

function deleteReservation(calEvent, jsEvent, view) {
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
    $("#calendar").fullCalendar({
        header: false,
        resources: 'reservation/fields/',
        defaultView: 'resourceDay',
        allDaySlot: false,
        minTime: '08:00:00',
        maxTime: '22:00:00',
        aspectRatio: 0.0,
        theme: true,
        editable: true,
        axisFormat: 'HH:mm',
        timeFormat: '',
        slotEventOverlap: false,
        slotDuration: '01:00:00',
        selectable: canSelect,
        selectHelper: true,
        select: addReservation,
        events: '/reservation/all/',
        eventClick: deleteReservation
    });
    $('#datepicker').datepicker({
        inline: true,
        minDate: 0,
        firstDay: 1,
        onSelect: function () {
            $('#calendar').fullCalendar('gotoDate', $('#datepicker').datepicker('getDate'));
        }
    });
});
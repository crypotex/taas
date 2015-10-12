var canSelect;

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
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

$(document).ready(function () {
    $("#calendar").fullCalendar({
        header: false,
        resources: 'reservation/get_fields/',
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
        select: function (start, end, ev) {
            jQuery.post('reservation/initialize/',
                {
                    start: start.format(),
                    end: end.format(),
                    field: ev.data.name
                },
                $("#calendar").fullCalendar('refetchEvents')
            );
        },
        events: '/reservation/get_events/'
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

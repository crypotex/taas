var testEvent;

function isOverlapping(event) {
    var events = $("#updateReservation").fullCalendar('clientEvents');
    var index;
    for (index = 0; index < events.length; ++index) {
        var oldEvent = events[index];
        var diff = oldEvent.start.diff(event.start, 'minutes');
        if (diff == 0 && oldEvent.id != event.id &&
            oldEvent.resources[0] == event.resources[0]) {
            return true;
        }
    }
    return false;
}

function onEventDrag(event, delta, revertFunc) {
    if (isOverlapping(event)) {
        revertFunc();
    } else {
        testEvent = event;
        $("#id_start").val(event.start.format('YYYY-MM-DD HH:mm'));
        $("#id_end").val(event.end.format('YYYY-MM-DD HH:mm'));
        $("#id_field").val(event.resources[0]);
    }
}

$(document).ready(function () {
    $("#updateReservation").fullCalendar({
        header: false,
        resources: '/reservation/fields/',
        defaultView: 'resourceDay',
        allDaySlot: false,
        minTime: '08:00:00',
        maxTime: '22:00:00',
        aspectRatio: 0.0,
        theme: true,
        axisFormat: 'HH:mm',
        timeFormat: '',
        slotDuration: '01:00:00',
        events: entities,
        eventDrop: onEventDrag,
        defaultDate: tableDate
    });
});
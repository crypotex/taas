$(document).ready(function() {

    // page is now ready, initialize the calendar...

    $('#calendar').fullCalendar({
        // put your options and callbacks here
        views: {
            multiColAgendaWeek: {
                type: 'multiColAgenda',
                duration: { weeks: 1 },
                numColumns: 3
            }
        },
        defaultView: 'multiColAgendaWeek',
        firstDay: 1,
        slotDuration: '01:00:00',
        slotEventOverlap: false,
        allDay: false,
        columnFormat: 'DD/MM',
        timeFormat: 'HH:mm { - HH:mm}',
        axisFormat: 'HH:mm',
        minTime: '08:00:00',
        maxTime: '22:00:00',
        contentHeight: 440,
        editable: true,
        header: {
            left: 'prev',
            center: 'title',
            right: 'next'
        },
        //hardcoded event at the moment
        events: [{
            title: 'Some event',
            start: $.fullCalendar.moment('2015-10-05T12:00:00'),
            end: $.fullCalendar.moment('2015-10-05T14:00:00'),
            column: 1
        }]
    });
});
$(document).ready(function() {

    // page is now ready, initialize the calendar...

    $('#calendar').fullCalendar({
        // put your options and callbacks here
        defaultView: 'agendaWeek',
        firstDay: 1,
        slotDuration: '01:00:00',
        slotEventOverlap: false,
        minTime: '08:00:00',
        maxTime: '22:00:00',
        contentHeight: 400
    })

});
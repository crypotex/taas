$(document).ready(function() {
    //pole vaja, aga et näha mingeid evente, siis jätan siia
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    $("#calendar").fullCalendar({
        header: false, //võib välja kommenteerida, et näha, kas datepicker'ist saadakse õige päev
        resources: [
            {
                'id': 'A',
                'name': 'A'
            }, {
                'id': 'B',
                'name': 'B'
            }, {
                'id': 'C',
                'name': 'C'
            }
        ],
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
        selectable: true,
        selectHelper: true,
        select: function(start, end, ev) {
            var title = prompt('Event Title:');
            if (title) {
                $('#calendar').fullCalendar('renderEvent',
                    {
                        title: title,
                        start: start,
                        end: end,
                        resources: ev.data
                    },
                    true // make the event "stick"
                );
                /*/!**
                 * ajax call to store event in DB
                 *!/
                jQuery.post(
                    "event/new" // your url
                    , { // re-use event's data
                        title: title,
                        start: start,
                        end: end,
                        allDay: allDay
                    }
                );*/
            }
            //$('#calendar').fullCalendar('unselect');
        },
        events: [{
         title: 'R1: Lunch 12.00-14.00',
         start: new Date(y, m, d, 12, 0),
         end: new Date(y, m, d, 14, 0),
         resources: 'A',
         editable: false
         }, {
         title: 'Lunch',
         start: new Date(y, m, d, 10, 0),
         end: new Date(y, m, d, 11, 0),
         resources: 'B',
         editable: false
         }, {
         title: 'Repeating Event',
         start: new Date(y, m, d + 3, 16, 0),
         end: new Date(y, m, d+3, 17, 0),
         resources: 'C',
         editable: false
         }]
    });

    $('#datepicker').datepicker({
        inline: true,
        minDate: 0,
        firstDay: 1,
        onSelect: function() {
            $('#calendar').fullCalendar('gotoDate', $('#datepicker').datepicker('getDate'));
        }
    });
});
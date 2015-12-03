var canSelect;var timeError;var expireMessage;var expireDate=null;swal.setDefaults({confirmButtonColor:"#ffa31a"});function setExpireDate(){jQuery.ajax({url:"/reservation/expire/",success:function(a){if(a.response){expireDate=new Date();expireDate.setMinutes(expireDate.getMinutes()+parseInt(a.response.split(":")[0]));expireDate.setSeconds(expireDate.getSeconds()+parseInt(a.response.split(":")[1]));startTimer(expireDate)}},async:false,cache:false})}function startTimer(a){document.getElementById("timerMessage").style.display="block";$("#timer").countdown(a,function(b){$(this).html(b.strftime("%M:%S"))}).on("finish.countdown",function(){stopTimer();removeReservationsOnExpire();disableSubmition();a=null;swal({title:"Warning",text:expireMessage,type:"warning",confirmButtonText:"OK"})})}function stopTimer(){document.getElementById("timerMessage").style.display="none";$("#timer").countdown("stop")}function disableSubmition(){document.getElementById("submitBookings").style.display="none"}function enableSubmition(){document.getElementById("submitBookings").style.display="block"}function removeReservationsOnExpire(){jQuery.post("/reservation/remove/all/").done(function(){$("#calendar").fullCalendar("refetchEvents")})}function addReservation(d,a,c){var b=d.diff(moment(),"minutes");if(b<30){swal({title:"Warning",text:timeError,type:"warning",customClass:"alert-button"})}else{jQuery.post("reservation/add/",{start:d.zone("+0200").format("YYYY-MM-DD HH:mm"),end:a.zone("+0200").format("YYYY-MM-DD HH:mm"),field:c.data.name}).done(function(){$("#calendar").fullCalendar("refetchEvents");if(!expireDate){expireDate=moment().add(10,"minutes").toDate()}startTimer(expireDate);enableSubmition()})}}function deleteReservation(a){if(a.color!="#b285e0"){return}jQuery.post("/reservation/remove/",{id:a.id},function(b){if(!b.response){disableSubmition();stopTimer();expireDate=null}},"json").done(function(){$("#calendar").fullCalendar("refetchEvents")})}$(document).ready(function(){$("#calendar").fullCalendar({header:false,resources:"reservation/fields/",defaultView:"resourceDay",allDaySlot:false,minTime:"08:00:00",maxTime:"22:00:00",aspectRatio:0,theme:true,axisFormat:"HH:mm",timeFormat:"",timezone:"local",slotDuration:"01:00:00",selectable:canSelect,selectHelper:true,select:addReservation,events:"/reservation/all/",eventClick:deleteReservation});$(".fc-col0").tooltipster({theme:"tooltipster-light",offsetX:-135,content:$(fieldA)});$(".fc-col1").tooltipster({theme:"tooltipster-light",offsetX:-135,content:$(fieldB)});$(".fc-col2").tooltipster({theme:"tooltipster-light",offsetX:-135,content:$(fieldC)});$("#datepicker").datepicker({inline:true,minDate:0,firstDay:1,onSelect:function(){$("#calendar").fullCalendar("gotoDate",$("#datepicker").datepicker("getDate"))}})});
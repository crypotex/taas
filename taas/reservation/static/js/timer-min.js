var expireDate=null;swal.setDefaults({confirmButtonColor:"#ffa31a"});function setExpireDate(){jQuery.ajax({url:"/reservation/expire/",success:function(a){if(a.response){expireDate=new Date();expireDate.setMinutes(expireDate.getMinutes()+parseInt(a.response.split(":")[0]));expireDate.setSeconds(expireDate.getSeconds()+parseInt(a.response.split(":")[1]));startTimer(expireDate)}},async:false,cache:false})}function startTimer(a){document.getElementById("timerMessage").style.display="block";$("#timer").countdown(a,function(b){$(this).html(b.strftime("%M:%S"))}).on("finish.countdown",function(){stopTimer();removeReservationsOnExpire();swal({title:"Warning",text:expireMessage,type:"warning",confirmButtonText:"OK"})})}function stopTimer(){document.getElementById("timerMessage").style.display="none";$("#timer").countdown("stop")}function removeReservationsOnExpire(){jQuery.post("/reservation/remove/all/").done(function(){stopTimer();swal({title:"Warning",text:expireMessage,type:"warning",confirmButtonText:"OK"})})};
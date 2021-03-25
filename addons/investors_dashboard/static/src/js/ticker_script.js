$(document).ready(function() {
console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>") ;
variable =  $('#my_chatter_feed') ;
console.log(variable);
if (typeof variable !== 'undefined') {
    // the variable is defined
    $(function() {
      $('#my_chatter_feed').vTicker();
    });
}


});
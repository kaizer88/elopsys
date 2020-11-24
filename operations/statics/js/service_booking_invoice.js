service_booking = {}

$(function() {
  $('#qoute_number, #qoute_amount, #qoute_date, #qoute_reason').hide(); 
    $(function() {
      $('#quote_received').change(function(){
          $('#qoute_reason')[ ($("option[value='no']").is(":checked"))? "show" : "hide" ]();
          $('#qoute_number, #qoute_amount, #qoute_date')[ ($("option[value='yes']").is(":checked"))? "show" : "hide" ](); 
          });
      });


    $('#id_long_term_repairs').change(function(){

    	$('#id_follow_up_date').hide(); 
    	$('label[for="id_follow_up_date"]').hide();
        
        if($('#id_long_term_repairs').prop('checked')){
        	$('#id_follow_up_date').show();
        	$('label[for="id_follow_up_date"]').show();
        }
        else{
        	$('#id_follow_up_date').hide();
        	$('label[for="id_follow_up_date"]').hide();
        }
    });

   $().ready(function(){
   	$('#id_follow_up_date').hide();
   	$('label[for="id_follow_up_date"]').hide();
    $('#id_drivers').prop('disabled', true);
    $('#id_balances').prop('disabled', true);

   	if($('#id_long_term_repairs').prop('checked')){
   		$('#id_follow_up_date').show();
   		$('label[for="id_follow_up_date"]').show();
   	}
   	else{
   		$('#id_follow_up_date').hide();
   		$('label[for="id_follow_up_date"]').hide();
   	}


    $('.multi_select').multiselect({ nonSelectedText: "None selected" });
    var vendor = $("#id_vendor").val();
    autoselect_service_booking_balances(vendor);
    $("#id_vendor").change(function(){
      autoselect_service_booking_balances($(this).val())
    });

    var vehicle = $("#id_vehicle").val();
    autoselect_current_driver(vehicle);
    $("#id_vehicle").change(function(){
      autoselect_current_driver($(this).val())
    });

   });

});

var autoselect_service_booking_balances = function(id) {   
   
    var url = '/get_service_booking_balances/' + id;
    $.getJSON(url, function(data) {            
        $('#id_balances').val(data.balances);
    });
};

var autoselect_current_driver = function(id) {

    var url = '/get_current_driver/' + id;
    $.getJSON(url, function(data) {
        $('#id_drivers').val(data.drivers);
    });
};
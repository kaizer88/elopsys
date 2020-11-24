incident = {}

incident.incident_document_delete = function(url) {
    $("#incident_document_delete_modal a.btn").attr("href", url);
}

$(function(){
  $().ready(function(){
    $("#id_driver, #id_share_amount,  #id_drivers_licence, #id_expiry_date").prop('disabled', true);
    $("#id_percentage, #id_status").prop('disabled', true);
    var status = $("#id_driver_co_payment option:selected").val();

    $("#id_percentage").change(function(){
      invoice_amount = $("#id_invoice_amount").val();
      percentage = $("#id_percentage").val();
      share_amount = (invoice_amount*percentage)/100;
      $("#id_share_amount").val(share_amount)
    });

    $("#id_driver_co_payment").change(function(){
      var status = $("#id_driver_co_payment option:selected").val();
      if(status=="yes"){
        $("#id_percentage").prop('disabled', false);
      }
      else{
        $("#id_percentage").prop('disabled', true);
      }
    });

    $("#id_vehicle").change(function(){
        autoselect_driver_licence($(this).val()),
        autoselect_driver_licence_expiry_date($(this).val())     
    });

    var vehicle_id = $("#id_vehicle").val()
        autoselect_driver_licence(vehicle_id),
        autoselect_driver_licence_expiry_date(vehicle_id)

    $('#id_incident_date').change(function(){
        var vehicle_id = $("#id_vehicle").val()
        if(vehicle_id != null){
          autoselect_driver_licence(vehicle_id),
          autoselect_driver_licence_expiry_date(vehicle_id)
        }        
    })

    if(status=="yes"){
      $("#id_percentage").prop('disabled', false);
    }
    else{
      $("#id_percentage").prop('disabled', true);
    }
  });
});

$(function(){
$().ready(function() {
  var status = $("#id_driver_co_payment option:selected").val();
  if (status=="yes") {
      $("#id_percentage").prop('disabled', false);
    }
    else
    {
      $("#id_percentage").prop('disabled', true);
    }
    
});
});

function d2(n) {
    if(n<9) return "0"+n;
    return n;
}

var autoselect_driver_licence =  function(id){
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth()+1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());
    
    var transaction_date = $('#id_incident_date').val() || sDate;    

    if (transaction_date != ""){
        var url = '/get_driver_licence/' + id;
        $.getJSON(url, {transaction_date:transaction_date}, function(data){
           
            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('#id_drivers_licence').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'select2:select',
                params: {
                    data: data
                }
            });               
        });
    }
};

var autoselect_driver_licence_expiry_date =  function(id){
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth()+1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());
    
    var transaction_date = $('#id_incident_date').val() || sDate;    

    if (transaction_date != ""){
        var url = '/get_driver_licence_expiry_date/' + id;
        $.getJSON(url, {transaction_date:transaction_date}, function(data){
           
            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('#id_expiry_date').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'select2:select',
                params: {
                    data: data
                }
            });               
        });
    }
};


$(function() {
    $('#id_status').change(status_change);
    status_change();

    $("#id_driver").change(function(){
        autoselect_vehicle($(this).val())
    });

    $('#id_date_used').change(function(){
        var driver_id = $("#id_driver").val()
        if(driver_id != null){
            autoselect_vehicle(driver_id)
        }        
    });

    $('.multi_select').multiselect({nonSelectedText:"None selected"});
});


status_change = function()
{
  stat = $('#id_status').val();
  if(stat == 'cancelled')
  {
    $('#cancelled').show();
    $('.cancelled').show();
  }
  else
  {
    $('#cancelled').hide();
    $('.cancelled').hide();
  }
}

function d2(n) {
    if(n<9) return "0"+n;
    return n;
}

var autoselect_vehicle =  function(id){
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth()+1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());
    
    var transaction_date = $('#id_date_used').val() || sDate;

    if (transaction_date != ""){
        var url = '/get_vehicle_of_driver/' + id;
        $.getJSON(url, {transaction_date:transaction_date}, function(data){
           
            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('.auto_select').append(option).trigger('change');

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


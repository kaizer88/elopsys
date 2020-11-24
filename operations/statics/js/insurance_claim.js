vehicle = {}

function d2(n) {
    if (n < 9) return "0" + n;
    return n;
}

var autoselect_driver = function(id) {
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth() + 1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != "") {
        var url = '/get_vehicle_driver/' + id;
        $.getJSON(url, { transaction_date: transaction_date }, function(data) {

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

var autoselect_vehicle_details = function(id) {   
   
    var url = '/get_vehicle_details/' + id;
    $.getJSON(url, function(data) {
            
        $('#id_division').val(data.division);
        $('#id_region').val(data.region);
        $('#id_district').val(data.district);
        $('#id_ownership').val(data.ownership);
        $('#id_vin_number').val(data.vin_number);
        $('#id_engine_number').val(data.engine_number);
        $('#id_colour').val(data.colour);
        $('#id_make').val(data.make);
        $('#id_model').val(data.model);
        $('#id_year_model').val(data.year_model);
    });
};


var autoselect_vehicle_division = function(id) {
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth() + 1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != "") {
        var url = '/get_vehicle_division/' + id;
        $.getJSON(url, { transaction_date: transaction_date }, function(data) {

            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            var test = $('#id_division').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'getJSON',
                params: {
                    data: data
                }
            });
        });
    }
};

var autoselect_vehicle_region = function(id) {
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth() + 1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != "") {
        var url = '/get_vehicle_region/' + id;
        $.getJSON(url, { transaction_date: transaction_date }, function(data) {

            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('#id_region').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'getJSON',
                params: {
                    data: data
                }
            });
        });
    }
};

var autoselect_vehicle_district = function(id) {
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth() + 1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != "") {
        var url = '/get_vehicle_district/' + id;
        $.getJSON(url, { transaction_date: transaction_date }, function(data) {

            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('#id_district').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'getJSON',
                params: {
                    data: data
                }
            });
        });
    }
};

var autoselect_vehicle_ownership = function(id) {
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth() + 1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != "") {
        var url = '/get_vehicle_ownership/' + id;
        $.getJSON(url, { transaction_date: transaction_date }, function(data) {

            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('#id_ownership').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'getJSON',
                params: {
                    data: data
                }
            });
        });
    }
};

var autoselect_vehicle_vin_number = function(id) {
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth() + 1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != "") {
        var url = '/get_vehicle_vin_number/' + id;
        $.getJSON(url, { transaction_date: transaction_date }, function(data) {

            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('#id_vin_number').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'getJSON',
                params: {
                    data: data
                }
            });
        });
    }
};

var autoselect_vehicle_engine_number = function(id) {
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth() + 1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != "") {
        var url = '/get_vehicle_engine_number/' + id;
        $.getJSON(url, { transaction_date: transaction_date }, function(data) {

            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('#id_engine_number').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'getJSON',
                params: {
                    data: data
                }
            });
        });
    }
};

var autoselect_vehicle_colour = function(id) {
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth() + 1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != "") {
        var url = '/get_vehicle_colour/' + id;
        $.getJSON(url, { transaction_date: transaction_date }, function(data) {

            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('#id_colour').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'getJSON',
                params: {
                    data: data
                }
            });
        });
    }
};

var autoselect_vehicle_make = function(id) {
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth() + 1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != "") {
        var url = '/get_vehicle_make/' + id;
        $.getJSON(url, { transaction_date: transaction_date }, function(data) {

            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('#id_make').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'getJSON',
                params: {
                    data: data
                }
            });
        });
    }
};

var autoselect_vehicle_model = function(id) {
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth() + 1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != "") {
        var url = '/get_vehicle_model/' + id;
        $.getJSON(url, { transaction_date: transaction_date }, function(data) {

            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('#id_model').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'getJSON',
                params: {
                    data: data
                }
            });
        });
    }
};

var autoselect_vehicle_year_model = function(id) {
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth() + 1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != "") {
        var url = '/get_vehicle_year_model/' + id;
        $.getJSON(url, { transaction_date: transaction_date }, function(data) {

            // create the option and append to Select2
            var option = new Option(data.value, data.id, true, true);
            $('#id_year_model').val(data.value);

            // manually trigger the `select2:select` event
            $('.auto_select').trigger({
                type: 'getJSON',
                params: {
                    data: data
                }
            });
        });
    }
};

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

$(function(){
    $().ready(function(){
        $('.multi_select').multiselect({ nonSelectedText: "None selected" });

        $("#id_vehicle").change(function(){
            autoselect_driver($(this).val())
        });
        var vehicle_id = $("#id_vehicle").val();
        autoselect_vehicle_details(vehicle_id); 
        autoselect_driver_licence(vehicle_id),
        autoselect_driver_licence_expiry_date(vehicle_id)

        $("#id_vehicle").change(function(){
            autoselect_vehicle_details($(this).val()),
            autoselect_driver_licence($(this).val()),
            autoselect_driver_licence_expiry_date($(this).val()) 
        });

        $("#id_incident_date").change(function(){
            var vehicle_id = $("#id_vehicle").val();
            if(vehicle_id != null){
                autoselect_driver(vehicle_id),
                autoselect_vehicle_details(vehicle_id);
                autoselect_driver_licence(vehicle_id),
                autoselect_driver_licence_expiry_date(vehicle_id)
            }
        });

        $("#id_reason_other").hide();
        $("#id_driver, #id_division, #id_region, #id_district, #id_ownership, #id_drivers_licence, #id_expiry_date").prop('disabled', true);
        $("#id_vin_number, #id_engine_number, #id_colour, #id_make, #id_model, #id_year_model").prop('disabled', true);
        $('label[for="id_reason_other"]').hide();

        $("#id_claim_type").change(function(){
            var status = $("#id_claim_type option:selected").val();

            if(status == "other"){
                $('#id_reason_other').show();
                $('label[for="id_reason_other"]').show();
            }
            else{
                $('#id_reason_other').hide();
                $('label[for="id_reason_other"]').hide();
            }
        });

        var status = $("#id_claim_type option:selected").val();
        if(status == "other"){
            $('#id_reason_other').show();
            $('label[for="id_reason_other"]').show();
        }
        else{
            $('#id_reason_other').hide();
            $('label[for="id_reason_other"]').hide();
        }

        $("#id_percentage").change(function(){
            invoice_amount = $("#id_invoice_amount").val();
            percentage = $("#id_percentage").val();
            share_amount = (invoice_amount*percentage)/100;
            $("#id_share_amount").val(share_amount);
        });

        $("#id_percentage, #id_status").prop('disabled', true);

        $("#id_driver_co_payment").change(function(){
            var status = $("#id_driver_co_payment option:selected").val();
            if(status=="yes"){
                $("#id_percentage").prop('disabled', false);
            }
            else{
                $("#id_percentage").prop('disabled', true);
            }
        });

        $("#id_share_amount").prop('disabled', true);
        var status = $("#id_driver_co_payment option:selected").val();
        if(status=="yes"){
            $("#id_percentage").prop('disabled', false)
        }
        else{
            $("#id_percentage").prop('disabled', true);
        }
});

});

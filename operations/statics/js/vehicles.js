vehicle = {}

vehicle.submit_document = function(el) {
    var vehicle_id = $(el).data('vehicle');
    var form = $(el).closest('form');
    $(form).attr('action',Urls['fleetmanagement:add_document'](vehicle_id));

    $(form).submit();
};

vehicle.submit_photo = function(el) {
    var vehicle_id = $(el).data('vehicle');
    var form = $(el).closest('form');
    $(form).attr('action',Urls['fleetmanagement:add_photo'](vehicle_id));

    $(form).submit();
};

vehicle.resolve_fine = function(url) {
    $("#resolve_fine_modal a.btn").attr("href", url);
}

vehicle.toggle_downloads_list = function () {

    if ($(".switch input[type='checkbox']").is(":checked")) {
    $(".downloads_table tr").removeClass('hidden');
    } else {
    $(".downloads_table tbody tr").not(".dl_user").addClass('hidden');
    }
}

$( function() {

    $('#myTab a').click(function(e) {
      e.preventDefault();
      $(this).tab('show');
    });

    $(".vehicle_document_upload").on('click', function() {
	vehicle.submit_document($(this));
    });

    $(".vehicle_photo_upload").on('click', function() {
    vehicle.submit_photo($(this));
    });

    //store the currently selected tab in the hash value
    $("ul.nav-pills > li > a").on("shown.bs.tab", function(e) {
      var id = $(e.target).attr("href").substr(1);
      window.location.hash = id;
    });

    // // on load of the page: switch to the currently selected tab
    var hash = window.location.hash;
    var isrm = $(':hidden[name=is_rm]').val()

    $('#myTab a[href="' + hash + '"]').tab('show');
        if($('#file_upload').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document, #unassign_fuel_card').removeClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('file_upload');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#vehicle_driver').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).removeClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#unassign_driver').removeClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#file_upload_document').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('vehicle_driver');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#fuel_card').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#fuel_card_history').removeClass('hidden');
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('fuel_card');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#details').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('details');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#extras').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('extras');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#vehicle_tyre').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').removeClass('hidden');
            $(':hidden[name=tab]').val('vehicle_tyre');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#purchase_detail').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('purchase_detail');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#tracker').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('tracker');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#branding').hasClass('active')) {
           if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('branding');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#service_booking').hasClass('active')) {
            $( "#save_vehicle" ).addClass('hidden');
            $( "#submit_for_authorization" ).addClass('hidden');
            $( "#authorize" ).addClass('hidden');
            $('#service_history').removeClass('hidden');
            $('#file_upload_document').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('service_booking');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#incidents').hasClass('active')) {
            $( "#save_vehicle" ).addClass('hidden');
            $( "#submit_for_authorization" ).addClass('hidden');
            $( "#authorize" ).addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#file_upload_document').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').removeClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('service_booking');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#insurance').hasClass('active')) {
            $( "#save_vehicle" ).addClass('hidden');
            $( "#submit_for_authorization" ).addClass('hidden');
            $( "#authorize" ).addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#file_upload_document').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').removeClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('service_booking');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else{
             $(':hidden[name=tab]').val('')
        }

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        if($('#file_upload').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').removeClass('hidden');
            $('#service_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('file_upload')
        }
        else if($('#vehicle_driver').hasClass('active')) {
           if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).removeClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#unassign_driver').removeClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#file_upload_document').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('vehicle_driver')
        }
        else if($('#fuel_card').hasClass('active')) {
            $( "#save_vehicle" ).addClass('hidden');
            $( "#submit_for_authorization" ).addClass('hidden');
            $( "#authorize" ).addClass('hidden');
            $('#fuel_card_history').removeClass('hidden');
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('fuel_card')
        }
        else if($('#details').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('details')
        }
        else if($('#extras').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('extras')
        }
        else if($('#vehicle_tyre').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').removeClass('hidden');
            $(':hidden[name=tab]').val('vehicle_tyre')
        }
        else if($('#purchase_detail').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('purchase_detail')
        }
        else if($('#tracker').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('tracker')
        }
        else if($('#branding').hasClass('active')) {
            if(isrm == "True"){ 
                $( "#save_vehicle" ).addClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }else{ 
                $( "#save_vehicle" ).removeClass('hidden');
                $( "#submit_for_authorization" ).addClass('hidden');
                $( "#authorize" ).addClass('hidden');
            }
            $('#file_upload_document').addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('branding')
        }
        else if($('#service_booking').hasClass('active')) {
            $( "#save_vehicle" ).addClass('hidden');
            $( "#submit_for_authorization" ).addClass('hidden');
            $( "#authorize" ).addClass('hidden');
            $('#file_upload_document').addClass('hidden');
            $('#service_history').removeClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('service_booking')
        }
        else if($('#incidents').hasClass('active')) {
            $( "#save_vehicle" ).addClass('hidden');
            $( "#submit_for_authorization" ).addClass('hidden');
            $( "#authorize" ).addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#file_upload_document').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').addClass('hidden');
            $('#incidents_history').removeClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('service_booking');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else if($('#insurance').hasClass('active')) {
            $( "#save_vehicle" ).addClass('hidden');
            $( "#submit_for_authorization" ).addClass('hidden');
            $( "#authorize" ).addClass('hidden');
            $('#service_history').addClass('hidden');
            $('#file_upload_document').addClass('hidden');
            $('#fuel_card_history').addClass('hidden');
            $('#unassign_driver').addClass('hidden');
            $('#insurance_history').removeClass('hidden');
            $('#incidents_history').addClass('hidden');
            $('#tyre_history').addClass('hidden');
            $(':hidden[name=tab]').val('service_booking');
            var reset_fields = $("#id_vehicle_driver-driver, #id_vehicle_driver-start_date, #id_vehicle_driver-reason").val("");
        }
        else{
             $(':hidden[name=tab]').val('')
        }

     });
});

vehicle.document_delete = function(url) {
    $("#document_delete_modal a.btn").attr("href", url);
}

var SelectCascade = ( function(window, $) {

    function SelectCascade(parent, child, url) {
        var afterActions = [];


        parent.on("change", function (e) {

            child.prop("disabled", true);

            var _this = this;
            $.getJSON(url.replace(':parentId:', $(this).val()), function(items) {
                if (child.hasClass("cascade")){
                    var newOptions = '<option value="">--- Select District ---</option>'
                }else{
                    var newOptions = '<option value="">-----</option>';
                }

                for(var id in items) {

                    newOptions += '<option value="'+ items[id].id +'">'+ items[id].label +'</option>';
                }

                child.empty().html(newOptions).prop("disabled", false)

            });
        });
    }

    return SelectCascade;

})( window, $);

function d2(n) {
    if(n<9) return "0"+n;
    return n;
}

vehicle.unassign_fuel_card = function(url) {
    $("#unassign_fuel_card_modal a.btn").attr("href", url);
}

var autoselect_driver =  function(id){
    today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth()+1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var transaction_date = $('#id_incident_date').val() || sDate;

    if (transaction_date != ""){
        var url = '/get_vehicle_driver/' + id;
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

var autoselect_fuel_card =  function(id){
   today = new Date();
    var sDate = today.getFullYear() + "-" + d2(parseInt(today.getMonth()+1)) + "-" + d2(today.getDate()) + " " + d2(today.getHours()) + ":" + d2(today.getMinutes());

    var url = '/get_vehicle_fuel_card/' + id;
    $.getJSON(url, function(data){

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

        $('#id_fuel_card-start_date').val(sDate);
    });
};

$(function(){

    $('.multi_select').multiselect({nonSelectedText:"None selected"});

    var cascadLoading = new SelectCascade($('#id_vehicle_make'), $('#id_vehicle_model'), "/get_vehicle_models/:parentId:");
    var cascadRegionDistrict = new SelectCascade($('#id_region'), $('#id_district'), "/get_districts/:parentId:");

    $("#id_vehicle").change(function(){
        autoselect_driver($(this).val())
    })
    $('#id_incident_date').change(function(){
        var vehicle_id = $("#id_vehicle").val()
        if(vehicle_id != null){
            autoselect_driver(vehicle_id)
        }
    })

    $("#purchase_type").change(function(){
        var purchase_type = $("#purchase_type option:selected").val();

        if (purchase_type=="cash") {
            $("#id_finance_detail-financier").prop('disabled', true);
        }
        else
        {
            $("#id_finance_detail-financier").prop('disabled', false);
        }
    })

    $('#id_vin_number').keyup(function(){
        var make = $("#id_vehicle_make option:selected").val();
        if (make == 1 || make == 2){
            $('#id_vin_number').attr('maxlength',17);
        }
        else{
            $('#id_vin_number').removeAttr('maxLength');
        }
        this.value = this.value.toUpperCase();
    });

    $('#id_maintenance').change(function(){

        if ($('#id_maintenance').prop('checked')){
            $('#maintenance_options').removeClass('hidden');
        }
        else{
            $('#maintenance_options').addClass('hidden');
            $("#id_tyres").prop("checked", false);
            $("#id_brakes").prop("checked", false);
            $("#id_clutch").prop("checked", false);
            $("#id_other").prop("checked", false);
        }
    })

    $('#id_service_bookings-maintenance').change(function(){

        if ($('#id_service_bookings-maintenance').prop('checked')){
            $('#maintenance_options').removeClass('hidden');
        }
        else{
            $('#maintenance_options').addClass('hidden');
            $("#id_service_bookings-tyres").prop("checked", false);
            $("#id_service_bookings-brakes").prop("checked", false);
            $("#id_service_bookings-clutch").prop("checked", false);
            $("#id_service_bookings-other").prop("checked", false);
        }
    })

});

$(function(){
    $().ready(function() {

        var purchase_type = $("#purchase_type option:selected").val();
        if (purchase_type=="cash") {
            $("#id_finance_detail-financier").prop('disabled', true);
        }
        else
        {
            $("#id_finance_detail-financier").prop('disabled', false);
        }

        if ($('#id_maintenance').prop('checked') == true){
            $('#maintenance_options').removeClass('hidden')
        }

        if ($('#id_maintenance').prop('checked') == false){
            $('#maintenance_options').addClass('hidden')
            $("#id_tyres").prop("checked", false);
            $("#id_brakes").prop("checked", false);
            $("#id_clutch").prop("checked", false);
            $("#id_other").prop("checked", false);
        }

        if ($('#id_service_bookings-maintenance').prop('checked') == true){
            $('#maintenance_options').removeClass('hidden')
        }

        if ($('#id_service_bookings-maintenance').prop('checked') == false){
            $('#maintenance_options').addClass('hidden')
            $("#id_service_bookings-tyres").prop("checked", false);
            $("#id_service_bookings-brakes").prop("checked", false);
            $("#id_service_bookings-clutch").prop("checked", false);
            $("#id_service_bookings-other").prop("checked", false);
        }

        var make = $("#id_vehicle_make option:selected").val();
        if (make == 1 || make == 2){
            $('#id_vin_number').attr('maxlength',17);
        }
        else{
            $('#id_vin_number').removeAttr('maxLength');
        }

    });
});

function ownership_selection(){
    var ownership_type = $('#id_ownership option:selected').val();
    if (ownership_type == "rental") {
	$('#all,#extras,#blank1').attr('hidden','hidden');
	$('#rental2,#rental3').removeAttr('hidden').removeClass('hidden');
    }else{
	$('#all,#extras,#blank1').removeAttr('hidden').removeClass('hidden');
	$('#rental2,#rental3').attr('hidden','hidden');
    }
    return ownership_type;
}

function paidby_selection(){
    var paid_by = $('#id_deposit_paid_by:selected').val();
    if (paid_by == "driver") {
	$('#id_deposit_driver').removeAttr('hidden').removeClass('hidden');
    }else{
	$('#id_deposit_driver').attr('hidden','hidden');
    }
    return paid_by;
}

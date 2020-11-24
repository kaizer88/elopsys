$(function() {
	$('[data-toggle="tooltip"]').tooltip(); 
	$(".datepicker").datepicker({'dateFormat':'yy-mm-dd' });
	$('.carousel').carousel();
	$('#id_current_mileage').change(calculateMileage);
	$('#id_actual_cost').change(calculateDifferance);
	$('#id_fuel_used').change(calculateFuelBalance);
	$('#id_amount_allocated').change(calculateNewBalance);
	$('#id_from_amount_allocated').change(calculateFromNewBalance);
	$('#id_to_amount_allocated').change(calculateToNewBalance);
	$('#id_log_date').change(getDates);
	$('#id_unit_price').change(calculateLineTotal);
	$("#all_fleet_table .btnSelect").on('click',function(){
	         // get the current row
				var currentRow=$(this).closest("tr");
				var col1=currentRow.find("td:eq(0)").data('id'); // get current row 1st TD value
				var modal_driver_value = col1 != null ? col1 : null;
				var modal_driver = $("select[name='driver'] option[value='"+modal_driver_value.toString()+"']");
				$(modal_driver).prop('selected', 'selected');
				$(modal_driver).trigger('change');        
					         	
   	});	

	$('[data-submenu]').submenupicker();

	$('form').on('submit',function(){
  		$('.load_spinner').css({'display': 'flex'});
	});	
	var select2Options = { width: 'resolve' };    
    
    $('#id_office').select2(select2Options);                 
    var cascadLoading = new Select2Cascade($('#id_office'), $('#id_floor'), "/get/floor/:parentId:", select2Options);   

    $('#id_floor').select2(select2Options);                 
    var cascadLoading = new Select2Cascade($('#id_floor'), $('#id_section'), "/get/section/:parentId:", select2Options);

});


var validate_driver = function(el) {
	var value = $(el).val();
	var param = $(el).attr('name')

	$("select[name='driver']").attr('onchange', '');

	if (param == "driver") {
		var params = {driver: value} 
	}

	$.get("/validate/driver/", params).done(function(data){
		// response_data = JSON.parse(data)
		console.log(data)
		if (param == "driver") {
			var driver = data.driver != null ? data.driver : null
			var has_no_licence = data.has_no_licence != null ? data.has_no_licence : null

			if (has_no_licence){
				$('#id_drivers_licence_prompt').html("<p style='color: red;'><i class='fa fa-exclamation-triangle' aria-hidden='true'></i> <label id='driver_name'>"+data.driver_name+"</label> has no driving licence loaded! <button name='lc_btn' id='id-lc-btn' type='button' class='btn btn-danger btn-xs' data-toggle='modal' data-target='#licenceModal'> Add Driving Licence</button></p>")
				$('#id_drivers_licence_prompt').removeClass('hidden');
				var modal_driver_value = data.driver != null ? data.driver : null
				var modal_driver = $("select[name='driver'] option[value='"+modal_driver_value.toString()+"']");
				$(modal_driver).prop('selected', 'selected');
				$(modal_driver).trigger('change');
				
			}
			else{
					$('#id_drivers_licence_prompt').addClass('hidden');
				}
		}			
		$("select[name='driver']").attr('onchange', 'validate_driver(this);');
	
	});
};

var pop_from_vehicle_info = function(el) {
	var value = $(el).val();
	var param = $(el).attr('name')

	$("select[name='from_driver'], select[name='from_vehicle']").attr('onchange', '');

	if (param == "from_driver") {
		var params = {from_driver: value} 
	} 
	else {
		var params = {from_vehicle: value} 
	}

	$.get('/get/from/trf/', params).done(function(data){
		// response_data = JSON.parse(data)
		console.log(data)
		if (param == "from_driver") {
			var from_vehicle_value = data.from_vehicle != null ? data.from_vehicle : null
			var from_vehicle = $("select[name='from_vehicle'] option[value='"+from_vehicle_value.toString()+"']");
			$(from_vehicle).prop('selected', 'selected');
			$(from_vehicle).trigger('change');

		} else {
			var from_driver_value = data.from_driver != null ? data.from_driver : null
			var from_driver = $("select[name='from_driver'] option[value='"+from_driver_value.toString()+"']");
			$(from_driver).prop('selected', 'selected');
			$(from_driver).trigger('change');
		}
		console.log(data.from_fuel_card.toString())
		var fuel_card = $("select[name='from_fuel_card'] option[value='"+data.from_fuel_card.toString()+"']");
		$(fuel_card).prop('selected', 'selected');
		$(fuel_card).trigger('change');

		$("[name='from_balance']").val(data.from_balance);	
		$("select[name='from_driver'], select[name='from_vehicle']").attr('onchange', 'pop_from_vehicle_info(this);');
	
	});
};

var pop_vehicle_info = function(el) {
	var value = $(el).val();
	var param = $(el).attr('name')

	$("select[name='driver'], select[name='vehicle']").attr('onchange', '');

	if (param == "driver") {
		var params = {driver: value} 
	} 
	else {
		var params = {vehicle: value} 
	}

	$.get('/get/to/trf/', params).done(function(data){
		// response_data = JSON.parse(data)
		console.log(data)
		if (param == "driver") {
			var vehicle_value = data.vehicle != null ? data.vehicle : null
			var vehicle = $("select[name='vehicle'] option[value='"+vehicle_value.toString()+"']");
			$(vehicle).prop('selected', 'selected');
			$(vehicle).trigger('change');		
		} else {
			var driver_value = data.driver != null ? data.driver : null
			var driver = $("select[name='driver'] option[value='"+driver_value.toString()+"']");
			$(driver).prop('selected', 'selected');
			$(driver).trigger('change');		
		}
		console.log(data)
		var fuel_card = $("select[name='to_fuel_card'] option[value='"+data.to_fuel_card.toString()+"']");
		$(fuel_card).prop('selected', 'selected');
		$(fuel_card).trigger('change');

		$("[name='to_balance']").val(data.to_balance);
		$("select[name='driver'], select[name='vehicle']").attr('onchange', 'pop_vehicle_info(this);');
		
	});
};

var Select2Cascade = ( function(window, $) {

    function Select2Cascade(parent, child, url, select2Options) {
        var afterActions = [];
        var options = select2Options || {};

        
        parent.select2(select2Options).on("change", function (e) {

            child.prop("disabled", true);

            var _this = this;
            $.getJSON(url.replace(':parentId:', $(this).val()), function(items) {
                var newOptions = '<option value="">-- Select --</option>';
                for(var id in items) {
                	
                    newOptions += '<option value="'+ items[id].id +'">'+ items[id].label +'</option>';
                }

                child.select2('destroy').html(newOptions).prop("disabled", false)
                    .select2(options);
                              
            });
        });
    }

    return Select2Cascade;

})( window, $);

calculateLineTotal = function()
{
	qty = parseInt($('#id_qty').val());
	up = parseInt($('#id_unit_price').val());
	lt = qty * up;
	$('#id_line_total').val(lt);
};

newTabToggle = function()
{
	console.log('newNextTab')
	var tab = $(".nav-tabs .tab-pane").not(".active")[0];
	$(".nav-tabs .tab-pane").removeClass("active");
	$(tab).addClass("active");
};

newPillToggle = function()
{
	console.log('newNextTab')
	var pill_view = $(".nav-pills .tab-pane").not(".active")[0];	
	$(".nav-pills .tab-pane").removeClass("active");
	$(pill_view).addClass("active");

	var pill = $(".pill_body .nav.nav-pills li").not(".active")[0];	
	$(".pill_body .nav.nav-pills li").removeClass("active");
	$(pill).addClass("active");
};


calculateMileage = function()
{
	current_mileage = parseInt($('#id_current_mileage').val());
	starting_mileage = parseInt($('#id_starting_mileage').val());
	mileage = current_mileage - starting_mileage;
	$('#id_mileage').val(mileage);
};

calculateDifferance = function()
{
	projected = parseInt($('#id_projected_cost').val());
	actual = parseInt($('#id_actual_cost').val());
	cost_diff = actual - projected;
	$('#id_difference').val(cost_diff);
};

calculateFuelBalance = function()
{
	balanceBf = parseInt($('#id_fuel_balance_bf').val());
	fuelUsed = parseInt($('#id_fuel_used').val());
	balance = balanceBf - fuelUsed;
	$('#id_fuel_balance').val(balance);
};

calculateNewBalance = function()
{
	balance = parseInt($('#id_balance').val());
	allocated = parseInt($('#id_amount_allocated').val());
	newbalance = allocated + balance;
	$('#id_new_balance').val(newbalance);
};

calculateFromNewBalance = function()
{
	bal = parseInt($('#id_from_balance').val());
	all = parseInt($('#id_from_amount_allocated').val());
	newbal = bal - all;
	$('#id_from_new_balance').val(newbal);
	$('#id_to_amount_allocated').val(all);
	tbal = parseInt($('#id_to_balance').val());	
	tnewbal = tbal + all;
	$('#id_to_new_balance').val(tnewbal);
};

calculateToNewBalance = function()
{
	balanc = parseInt($('#id_to_balance').val());
	allocatd = parseInt($('#id_to_amount_allocated').val());
	newbalanc = allocatd + balanc;
	$('#id_to_new_balance').val(newbalanc);
};


getDates =  function()	

{
	logDate = $('#id_log_date').val();
	startDate = moment(logDate,'YYYY-MM-DD').startOf('isoWeek').subtract(1, 'week').format('YYYY-MM-DD');		
	endDate = moment(startDate,"YYYY-MM-DD").add(6, 'day').format('YYYY-MM-DD');
	
	$('#id_start_date').val(startDate);
	$('#id_end_date').val(endDate);
};


loadTripLog = function(el, url) 
{
    $.post(url, function(data, status) {
       $(".trip_log_table").html(data);
    });
};





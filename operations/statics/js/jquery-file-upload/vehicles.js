vehicle = {}


vehicle.load_purchase_detail = function(vehicle_id) {

	$.get(Urls['app:purchase_detail_url']('vehicle_id', vehicle_id), function(response){

		var content = JSON.parse(response);

		$('pd_element').html(content);

	});
}

$( function() {



});
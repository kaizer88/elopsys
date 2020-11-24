
$(function() {
	$(':disabled').each(
	    function()
	    {
	        $(this).after('<input type="hidden" name="' + $(this).attr('name') + '" value="' + $(this).val() + '" />');
	    }
	);
    
    $("#id_stock_item").change(function(){
        autofill_opening_balance($(this).val())
    });

    $('.multi_select').multiselect({nonSelectedText:"None selected"});

    $("#id_transaction_type").change(function(){
        display_or_hide()
    });

    display_or_hide();
});


var autofill_opening_balance = function(id){
    var url = '/get_opening_balance/' + id;
    $.getJSON(url, function(data){
        $('.autofill_balance').val(data.value)
    })
};

var display_or_hide = function(){
    transaction = $('#id_transaction_type').val();
    if (transaction == 'allocated'){
        $('#supplier').addClass('hidden');
        $('#district').removeClass('hidden');
    }else if (transaction == 'received'){
        $('#supplier').removeClass('hidden');
        $('#district').addClass('hidden');
    }else{
        $('#supplier').removeClass('hidden');
        $('#district').removeClass('hidden');
    }
};

var stock_item_delete = function(url) {
    $("#stock_item_delete_modal a.btn").attr("href", url);
}

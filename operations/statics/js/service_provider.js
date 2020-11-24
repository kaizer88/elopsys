service_provider = {}


$().ready(function(){
    $("#id_balance").hide();
    $('label[for="id_balance"]').hide();

    $("#id_account_type").change(function(){
        var status = $("#id_account_type option:selected").val();
        if (status!="cash") {
            $("#id_balance").show();
        	$('label[for="id_balance"]').show();
        }
        else{
            $("#id_balance").hide();
        	$('label[for="id_balance"]').hide()
        }

    });

    var status = $("#id_account_type option:selected").val();
    if (status != "cash") {
        $("#id_balance").show();
        $('label[for="id_balance"]').show();
    }
    else{
        $("#id_balance").hide();
        $('label[for="id_balance"]').hide();
    }

          
    $("#account_type :input").attr("disabled", true);
    $("#balance :input").attr("disabled", true);
});


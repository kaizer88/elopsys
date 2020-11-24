assets = {}

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

$( document ).ready(function() {

  $('a[data-toggle="tab"]').on('show.bs.tab', function(e) {
    localStorage.setItem('activeTab', $(e.target).attr('href'));
  });
  var activeTab = localStorage.getItem('activeTab');
  if(activeTab){
    $('#myTab a[href="' + activeTab + '"]').tab('show');
  }

  var cascadRegionDistrict = new SelectCascade($('#id_region'), $('#id_district'), "/get_districts/:parentId:");

  var test = $('#id_category_one').val();
  if (test=="stationery"){
    $("#id_quantity").attr("disabled", false);
    $("#id_serial_number").attr("disabled", true);
  }
  else{
    $("#id_quantity").attr("disabled", true);
    $("#id_serial_number").attr("disabled", false);
  }
  
  $("#id_category_one").change(function(){
    var status = $('#id_category_one').val();
    if (status=="stationery") {
      $("#id_quantity").attr("disabled", false);
      $("#id_serial_number").attr("disabled", true);
    }
    else{
      $("#id_quantity").attr("disabled", true);
      $("#id_serial_number").attr("disabled", false);
    }

  });

});



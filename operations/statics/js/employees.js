vehicle = {}

$( function() {    
    $('#myTab a').click(function(e) {
      e.preventDefault();
      $(this).tab('show');
    });    

    //store the currently selected tab in the hash value
    $("ul.nav-pills > li > a").on("shown.bs.tab", function(e) {
      var id = $(e.target).attr("href").substr(1);
      window.location.hash = id;
    });

    // // on load of the page: switch to the currently selected tab
    var hash = window.location.hash;
    
    $('#myTab a[href="' + hash + '"]').tab('show');
        if($('#employee').hasClass('active')) {
            $('#vehicle_history').removeClass('hidden');
            $('#driving_licence_history').addClass('hidden');
            $(':hidden[name=tab]').val('employee');
        }
        else if($('#licence').hasClass('active')) {
            $('#driving_licence_history').removeClass('hidden');   
            $('#vehicle_history').addClass('hidden');
            $(':hidden[name=tab]').val('licence');   
        }
        else if($('#traffic').hasClass('active')) {             
           $('#vehicle_history').addClass('hidden');
           $('#driving_licence_history').addClass('hidden');
           $(':hidden[name=tab]').val('traffic');
        }
        else if($('#incidents').hasClass('active')) {         
            $('#vehicle_history').addClass('hidden');
            $(':hidden[name=tab]').val('incidents');
        } 
        else if($('#insurance').hasClass('active')) {         
          $('#vehicle_history').addClass('hidden');
          $('#driving_licence_history').addClass('hidden');
          $(':hidden[name=tab]').val('insurance');
        }        

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        if($('#employee').hasClass('active')) {
            $('#vehicle_history').removeClass('hidden');
            $('#driving_licence_history').addClass('hidden');
            $(':hidden[name=tab]').val('employee');
        }
        else if($('#licence').hasClass('active')) {
            
            $('#driving_licence_history').removeClass('hidden');  
            $('#vehicle_history').addClass('hidden');  
            $(':hidden[name=tab]').val('licence');  
        }
        else if($('#traffic').hasClass('active')) {             
           $('#vehicle_history').addClass('hidden');
           $('#driving_licence_history').addClass('hidden');
           $(':hidden[name=tab]').val('traffic');
        }
        else if($('#incidents').hasClass('active')) {         
            $('#vehicle_history').addClass('hidden');
            $('#driving_licence_history').addClass('hidden');
            $(':hidden[name=tab]').val('incidents');
        } 
        else if($('#insurance').hasClass('active')) {         
          $('#vehicle_history').addClass('hidden');
          $('#driving_licence_history').addClass('hidden');
          $(':hidden[name=tab]').val('insurance');
        }        

     });    
});


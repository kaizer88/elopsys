$(function() {

    $('.date_field').not('.birth_date').datetimepicker({
	format: 'yyyy-mm-dd',
	minView:'month',
	autoclose: true,
	forceParse:true,
	startView: 4,
    });

    $('.year_field').datetimepicker({
	format: 'yyyy',
	startView: 4,
	minView: 4,
	autoclose: true,
    });

    $('.birth_date').datetimepicker({
	format: 'yyyy-mm-dd',
	minView:'month',
	autoclose: true,
	forceParse:true,
	startView: 4,
    });
    
    $('.date_time_field').datetimepicker({autoclose: true});
    
    // OVERRIDE DATEPICKER HTML
    $('.datetimepicker table.table-condensed').addClass('table').removeClass('table-condensed');
    
    $('#extract_modal').modal({show: false});
    $('#load_modal').on('click', function(e){
      $('#extract_modal').modal('show');
      e.preventDefault()
    });

    $('#extract').on('click', function(){
      $('#extract_modal').modal('hide');
    })

    $('#myTab a').click(function(e) {
      e.preventDefault();
      $(this).tab('show');
    });

    // store the currently selected tab in the hash value
    $("ul.nav-tabs > li > a").on("shown.bs.tab", function(e) {
      var id = $(e.target).attr("href").substr(1);
      window.location.hash = id;
    });

    // on load of the page: switch to the currently selected tab
    var hash = window.location.hash;
    $('#myTab a[href="' + hash + '"]').tab('show');
});


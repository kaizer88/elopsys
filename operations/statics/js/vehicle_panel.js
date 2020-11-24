
open_side_panel = function() {
    $('#side_panel').css({ 'width': '20%' }),

        $('#main').css({ 'marginLeft': '20%' }),
        $('#nav_tabs').css({ 'padding-top': '2%' }),
        $('#container-fluid2').css({ 'marginLeft': '20%' }),

        $('#container').css({ 'marginLeft': '20%', 'padding-right':'25%', 'padding-top':'2%'}),
        $('#open_icon').css({ 'display': 'none' });
}

close_side_panel = function() {
    $('#side_panel').css({ 'width': '0' }),

        $('#main').css({ 'marginLeft': '0' }),
        $('#nav_tabs').css({ 'padding-top': '0%' }),
        $('#container-fluid2').css({ 'marginLeft': '0' }),

        $('#container').css({ 'marginLeft': '0', 'padding-right':'15%', 
        'padding-right':'75px', 'padding-top':'1%'}),
        $('#open_icon').css({ 'display': 'inline-block' });
}

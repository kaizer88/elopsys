$(function() {


    Morris.Donut({
        element: 'vehicle-service-chart',
        data:[
            {label: "Next Service (KM)", value: 100000},
            {label: "Current Mileage (KM)", value: 92000},
        ],
	colors: ['#aa1717','#5EAA16'],
    });


    Morris.Line({
	element: 'vehicle-mileage-line',
	data: [
	    { y: '2017-07', a: 11109 },
	    { y: '2017-08', a: 14098 },
	    { y: '2017-09', a: 8873 },
	    { y: '2017-10', a: 12989 },
	    { y: '2017-11', a: 6087 }
	],
	xkey: 'y',
	ykeys: 'a',
	labels: ['Mileage'],
	lineColors: ['#495fad', '#FFF']
    });

    Morris.Line({
	element: 'fuel-usage-line',
	data: [
	    { y: '2017-07', a: 50 },
	    { y: '2017-08', a: 40 },
	    { y: '2017-09', a: 30 },
	    { y: '2017-10', a: 5 },
	    { y: '2017-11', a: 60 }
	],
	xkey: 'y',
	ykeys: 'a',
	labels: ['Fuel'],
	lineColors: ['#495fad', '#FFF']
    });
});

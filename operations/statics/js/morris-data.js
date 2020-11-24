    stats={}
    vehicleStats={}
    insuranceStats={}

    $(function() {      
        
        
        while( stats.indexOf('&#39;')>-1 ){
            stats = stats.replace('&#39;','"')
        }
        json_stats = JSON.parse(stats)


        while( vehicleStats.indexOf('&#39;')>-1 ){
            vehicleStats = vehicleStats.replace('&#39;','"')
        }    
        json_vehicles = JSON.parse(vehicleStats) 


        while( insuranceStats.indexOf('&#39;')>-1 ){
            insuranceStats = insuranceStats.replace('&#39;','"')
        }   
        json_insurance = JSON.parse(insuranceStats) 

        Morris.Area({
            element: 'morris-area-chart',
            data: json_stats,
            xkey: 'period',
            ykeys: ['service', 'tires', 'repairs'],
            labels: ['Service', 'Tyres', 'Repairs'],
            pointSize: 2,
            hideHover: 'auto',
            resize: true
        });

        Morris.Bar({
            element: 'morris-bar-chart',
            data: json_vehicles,
            xkey: 'region',
            ykeys: ['fleet', 'leased'],
            labels: ['EL Fleet', 'EL Leased'],
            hideHover: 'auto',
            resize: true
        });        

        Morris.Donut({
            element: 'vehicle-service-chart',
            data:[
                {label: "Next Service", value: '100000'},
                {label: "Current Mileage", value: '84897'},
            ],
            resize: true
        });
        
        
    });

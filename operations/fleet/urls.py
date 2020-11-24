from django.conf.urls import url, handler400, handler403, handler404, handler500
from . import views
from . models import VehicleMaintenance, InsuranceClaim, RenewLicenceDisk, FuelAllocation, FuelTransfer

handler400 = 'fleet.views.handler400'
handler403 = 'fleet.views.handler403'
handler404 = 'fleet.views.handler404'
handler500 = 'fleet.views.handler500'

urlpatterns = [
    url(r'^fleet/add/vehicle/$', views.addvehicle, name='addvehicle'), 
    url(r'^get/from/trf/$', views.getFromFuelTrfDetails, name='get_fromtrf'),
    url(r'^get/to/trf/$', views.getToFuelTrfDetails, name='get_totrf'),
    url(r'^validate/driver/$', views.validateDriver, name='validate_driver'),   
    url(r'^fleet/edit/vehicle/(?P<vehicle_id>\-{0,1}\d+$)', views.editvehicle, name='editvehicle'),
    url(r'^fleet/view/vehicle/(?P<vehicle_id>\-{0,1}\d+$)', views.viewvehicle, name='viewvehicle'),   
    url(r'^fleet/view/vehicle-details/(?P<vehicle_id>\-{0,1}\d+$)', views.viewvehicleDetails, name='viewvehicleDetails'),     
    url(r'^fleet/view/vehicles-list/$', views.vehiclesList, name='vehiclesList'),

    url(r'^fleet/edit/driving-licence/(?P<trans_id>\-{0,1}\d+$)', views.editDrivingLicence, name='edit_drivinglicence'),
    url(r'^fleet/view/driving-licences-list/$', views.drivingLicencesList, name='view_drivinglicences'),
    url(r'^fleet/view/driver-profile/(?P<driver_id>\-{0,1}\d+$)', views.viewDriverProfile, name='view_driverprofile'), 
    
    url(r'^fleet/allocate/vehicle/(?P<vehicle_id>\-{0,1}\d+$)', views.allocatevehicle, name='allocatevehicle'),
    url(r'^allocate/vehicle/(?P<vehicle_id>\-{0,1}\d)/(?P<driver_id>\-{0,1}\d+$)', views.allocatevehicle_redirected, name='allocatevehicle_redirected'),
    url(r'^fleet/edit/vehicle-allocation/(?P<trans_id>\-{0,1}\d+$)', views.editallocatevehicle, name='editallocatevehicle'),
    url(r'^fleet/view/vehicle-allocation/(?P<trans_id>\-{0,1}\d+$)', views.viewallocatevehicle, name='viewallocatevehicle'),
    url(r'^fleet/view/vehicle-allocations-list/$', views.fleetAllocationsList, name='fleetAllocationsList'),

    url(r'^fleet/add/service-booking/(?P<vehicle_id>\-{0,1}\d+$)', views.bookservice, name='bookservice'),
    url(r'^fleet/edit/service-booking/(?P<trans_id>\-{0,1}\d+$)', views.editbookservice, name='editbookservice'),
    url(r'^fleet/view/service-booking/(?P<trans_id>\-{0,1}\d+$)', views.viewbookservice, name='viewbookservice'),
    url(r'^fleet/view/service-bookings-list/$', views.servicebookingsList, name='servicebookingsList'),

    url(r'^fleet/add/traffic-fine/(?P<vehicle_id>\-{0,1}\d+$)', views.trafficfines, name='trafficfines'),
    url(r'^fleet/edit/traffic-fine/(?P<trans_id>\-{0,1}\d+$)', views.edittrafficfines, name='edittrafficfines'),
    url(r'^fleet/view/traffic-fine/(?P<trans_id>\-{0,1}\d+$)', views.viewtrafficfines, name='viewtrafficfines'),
    url(r'^fleet/view/traffic-fines-list/$', views.trafficfinesList, name='trafficfinesList'),

    url(r'^fleet/add/vehicle-inspection/(?P<vehicle_id>\-{0,1}\d+$)', views.mileagelog, name='mileagelog'),
    url(r'^fleet/edit/vehicle-inspection/(?P<trans_id>\-{0,1}\d+$)', views.editmileagelog, name='editmileagelog'),
    url(r'^fleet/view/vehicle-inspection/(?P<trans_id>\-{0,1}\d+$)', views.viewmileagelog, name='viewmileagelog'),
    url(r'^fleet/view/vehicle-inspections-list/$', views.mileagelogList, name='mileagelogList'),

    url(r'^fleet/add/vehicle-maintenance/(?P<vehicle_id>\-{0,1}\d+$)', views.vehiclemaintenance, name='vehiclemaintenance'),
    url(r'^fleet/edit/vehicle-maintenance/(?P<trans_id>\-{0,1}\d+$)', views.editvehiclemaintenance, name='editvehiclemaintenance'),
    url(r'^fleet/view/vehicle-maintenance/(?P<trans_id>\-{0,1}\d+$)', views.viewvehiclemaintenance, name='viewvehiclemaintenance'),
    url(r'^fleet/view/vehicle-maintenance-list/$', views.vehiclemaintenanceList, name='vehiclemaintenanceList'),
   
    url(r'^fleet/requisition/vehicle/maintenance/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':VehicleMaintenance}, name='requisition_vehiclemaintenance'),
    url(r'^fleet/requisition/vehicle/insurance/excess/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':InsuranceClaim}, name='requisition_insuranceclaimexcess'),    
    url(r'^fleet/requisition/vehicle/licencing/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':RenewLicenceDisk}, name='requisition_vehiclelicencing'),
    url(r'^fleet/requisition/vehicle/fuel/allocation/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':FuelAllocation}, name='requisition_vehiclefuelallocation'),
    url(r'^fleet/requisition/vehicle/fuel/transfer/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':FuelTransfer}, name='requisition_vehiclefueltransfer'),
    url(r'^fleet/requisition/vehicle/trafficfine/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':VehicleMaintenance}, name='requisition_vehicletrafficfine'),

    url(r'^fleet/requisition/item/(?P<obj_id>\-{0,1}\d+$)', views.requisition_item, name='requisition_item'),
    url(r'^fleet/view/requisition/(?P<obj_id>\-{0,1}\d+$)', views.view_requisition, name='view_requisition'),
   
    url(r'^fleet/add/licence-disk-renewal/(?P<vehicle_id>\-{0,1}\d+$)', views.renewlicencedisk, name='renewlicencedisk'),
    url(r'^fleet/edit/licence-disk-renewal/(?P<trans_id>\-{0,1}\d+$)', views.editrenewlicencedisk, name='editrenewlicencedisk'),
    url(r'^fleet/view/licence-disk-renewal/(?P<trans_id>\-{0,1}\d+$)', views.viewrenewlicencedisk, name='viewrenewlicencedisk'),
    url(r'^fleet/view/licence-disk-renewals-list/$', views.licenceDiskRenewalList, name='licenceDiskRenewalList'),
    
    url(r'^fleet/add/vehicle-incident/(?P<vehicle_id>\-{0,1}\d+$)', views.vehicleincidences, name='vehicleincidences'),
    url(r'^fleet/edit/vehicle-incident/(?P<trans_id>\-{0,1}\d+$)', views.editvehicleincidences, name='editvehicleincidences'),
    url(r'^fleet/view/vehicle-incident/(?P<trans_id>\-{0,1}\d+$)', views.viewvehicleincidences, name='viewvehicleincidences'),
    url(r'^fleet/view/vehicle-incidences-list/$', views.incidencesList, name='incidencesList'),

    url(r'^fleet/add/vehicle-claim/(?P<vehicle_id>\-{0,1}\d+$)', views.addVehicleClaim, name='addVehicleClaim'),
    url(r'^fleet/view/vehicle-claim(?P<trans_id>\-{0,1}\d+$)', views.editVehicleClaim, name='viewVehicleClaim'),
    url(r'^fleet/edit/vehicle-claim(?P<trans_id>\-{0,1}\d+$)', views.viewVehicleClaim, name='editVehicleClaim'),   
    url(r'^fleet/view/vehicle-claims-list/$', views.vehicleClaimsList, name='vehicleClaimsList'), 

    url(r'^fleet/fuelcard/$', views.fuelcard, name='fuelcard'), 
    url(r'^fleet/allocate/fuel/(?P<vehicle_id>\-{0,1}\d+$)', views.allocatefuel, name='allocatefuel'),
    url(r'^fleet/edit/allocate/fuel/(?P<trans_id>\-{0,1}\d+$)', views.editallocatefuel, name='editallocatefuel'),

    url(r'^fleet/fueltransfer/$', views.fuelTransfer, name='fuel_transfer'), 

    url(r'^fleet/tripLog/Imports/(?P<vehicle_id>\-{0,1}\d+$)', views.tripLogImports, name='tripLogImports'),
    url(r'^fleet/loadtriplog/(?P<trip_id>\-{0,1}\d+$)', views.load_trip_log, name='load_trip_log'),

    url(r'^fleet/page_carousel/$', views.page_carousel, name='page_carousel'),  
    url(r'^fleet/get_fuel_card/$', views.get_fuel_card, name='get_fuel_card'),
    url(r'^fleet/get_employee/$', views.get_employee, name='get_employee'), 
    url(r'^fleet/get_vehicle/$', views.get_vehicle, name='get_vehicle'),
    url(r'^fleet/get_region/$', views.get_region, name='get_region'),

    url(r'^fleet/reports/current_drivers/$', views.rpt_current_drivers, name='rpt_current_drivers'), 
    url(r'^fleet/reports/vehicle_allocations/$', views.rpt_vehicle_allocations, name='rpt_vehicle_allocations'), 
    url(r'^fleet/reports/vehicle_fuel_allocations/$', views.rpt_vehicle_fuel_allocations, name='rpt_vehicle_fuel_allocations'), 
    url(r'^fleet/reports/vehicle_mileages/$', views.rpt_vehicle_mileages, name='rpt_vehicle_mileages'), 
    url(r'^fleet/reports/mileage_aggregates/$', views.rpt_mileage_aggregates, name='rpt_mileage_aggregates'), 
    url(r'^fleet/reports/driver_mileages/$', views.rpt_driver_mileages, name='rpt_driver_mileages'),
    url(r'^fleet/reports/driver_vehicle_allocations/$', views.rpt_driver_vehicle_allocations, name='rpt_driver_vehicle_allocations'),
    url(r'^fleet/reports/driver_fuel_allocations/$', views.rpt_driver_fuel_allocations, name='rpt_driver_fuel_allocations'),
    url(r'^fleet/reports/service_due/$', views.rpt_service_due, name='rpt_service_due'),
    url(r'^fleet/reports/service_overdue/$', views.rpt_service_overdue, name='rpt_service_overdue'),
    url(r'^fleet/reports/licence_disks_due/$', views.rpt_licence_disks_due, name='rpt_licence_disks_due'),
    url(r'^fleet/reports/licence_disks_expired/$', views.rpt_licence_disks_expired, name='rpt_licence_disks_expired'),
    url(r'^fleet/reports/vehicle_traffic_fines/$', views.rpt_vehicle_traffic_fines, name='rpt_vehicle_traffic_fines'),
    url(r'^fleet/reports/driver_traffic_fines/$', views.rpt_driver_traffic_fines, name='rpt_driver_traffic_fines'),    
    url(r'^fleet/reports/vehicle_maintenance/$', views.rpt_vehicle_maintenance, name='rpt_vehicle_maintenance'),
    url(r'^fleet/reports/vehicle_insurance_claims/$', views.rpt_vehicle_insurance_claims, name='rpt_vehicle_insurance_claims'),
    url(r'^fleet/reports/vehicle_incidences/$', views.rpt_vehicle_incidences, name='rpt_vehicle_incidences'),
    url(r'^fleet/reports/driver_incidences/$', views.rpt_driver_incidences, name='rpt_driver_incidences'),

    
    url(r'^fleet/authorizations/$', views.authorizations, name='authorizations'),
    url(r'^fleet/comments/$', views.comments, name='comments'),

        
    url(r'^fleet/redirect_from_comment/$', views.redirect_from_comment, name='redirect_from_comment'),    
]

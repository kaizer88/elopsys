from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from dal import autocomplete

import views
from fleet_management.autocomplete import *

from .models import *
from employees.models import *
from operations.models import *
from facilities.models import *

urlpatterns = [

    url(r'^vehicle-autocomplete/$', VehicleAutocomplete.as_view(model=Vehicle), name='vehicle-autocomplete'),
    url(r'^driver-autocomplete/$', DriverAutocomplete.as_view(model=Employee), name='driver-autocomplete'),
    url(r'^fuel_card-autocomplete/$', FuelCardAutocomplete.as_view(model=FuelCard), name='fuel_card-autocomplete'), 
    url(r'^fuel_card-autocomplete-filtered/(?P<vehicle_id>\d+)/$', FuelCardAutocomplete.as_view(model=FuelCard), name='fuel_card-autocomplete-filtered'),
    url(r'^vendor_tracker-autocomplete/$', VendorTrackerAutocomplete.as_view(model=Vendor), name='vendor_tracker-autocomplete'),
    url(r'^vendor_purchase_detail-autocomplete/$', VendorPurchaseDetailAutocomplete.as_view(model=Vendor), name='vendor_purchase_detail-autocomplete'),
    url(r'^vendor_service_provider-autocomplete/$', VendorServiceMaintenanceAutocomplete.as_view(model=Vendor), name='vendor_service_provider-autocomplete'),
    url(r'^vendor_fuel_card_supplier-autocomplete/$', VendorFuelCardSupplierAutocomplete.as_view(model=Vendor), name='vendor_fuel_card_supplier-autocomplete'),
    url(r'^vendor_insurance-autocomplete/$', VendorInsuranceAutocomplete.as_view(model=Vendor), name='vendor_insurance-autocomplete'), 
    url(r'^stock_item-autocomplete/$', StockItemAutocomplete.as_view(model=StockItem), name='stock_item-autocomplete'),

    url(r'^get_vehicle_models/(?P<make_id>\d+)/$', views.get_vehicle_models, name='get_vehicle_models'),  
    url(r'^get_vehicle_driver/(?P<vehicle_id>\d+)/$', views.get_vehicle_driver, name='get_vehicle_driver'),

    url(r'^get_vehicle_of_driver/(?P<driver_id>\d+)/$', views.get_vehicle_of_driver, name='get_vehicle_of_driver'),
    url(r'^get_vehicle_details/(?P<vehicle_id>\d+)/$', views.get_vehicle_details, name='get_vehicle_details'),
    url(r'^get_vehicle_division/(?P<vehicle_id>\d+)/$', views.get_vehicle_division, name='get_vehicle_division'),
    url(r'^get_vehicle_region/(?P<vehicle_id>\d+)/$', views.get_vehicle_region, name='get_vehicle_region'),
    url(r'^get_vehicle_district/(?P<vehicle_id>\d+)/$', views.get_vehicle_district, name='get_vehicle_district'),
    url(r'^get_vehicle_ownership/(?P<vehicle_id>\d+)/$', views.get_vehicle_ownership, name='get_vehicle_ownership'),

    url(r'^get_vehicle_vin_number/(?P<vehicle_id>\d+)/$', views.get_vehicle_vin_number, name='get_vehicle_vin_number'),
    url(r'^get_vehicle_engine_number/(?P<vehicle_id>\d+)/$', views.get_vehicle_engine_number, name='get_vehicle_engine_number'),
    url(r'^get_vehicle_colour/(?P<vehicle_id>\d+)/$', views.get_vehicle_colour, name='get_vehicle_colour'),
    url(r'^get_vehicle_make/(?P<vehicle_id>\d+)/$', views.get_vehicle_make, name='get_vehicle_make'),
    url(r'^get_vehicle_model/(?P<vehicle_id>\d+)/$', views.get_vehicle_model, name='get_vehicle_model'),
    url(r'^get_vehicle_year_model/(?P<vehicle_id>\d+)/$', views.get_vehicle_year_model, name='get_vehicle_year_model'),

    url(r'^get_vehicle_fuel_card/(?P<fuel_card_id>\d+)/$', views.get_vehicle_fuel_card, name='get_vehicle_fuel_card'),
    url(r'^get_current_vehicle_driver/(?P<vehicle_id>\d+)/$', views.get_current_vehicle_driver, name='get_current_vehicle_driver'),
    url(r'^get_districts/(?P<region_id>\d+)/$', views.get_districts, name='get_districts'),

    
    url(r'^get_driver_licence/(?P<vehicle_id>\d+)/$', views.get_driver_licence, name='get_driver_licence'),
    url(r'^get_driver_licence_expiry_date/(?P<vehicle_id>\d+)/$', views.get_driver_licence_expiry_date, name='get_driver_licence_expiry_date'),
    
    url(r'^get_service_booking_balances/(?P<vendor_id>\d+)/$', views.get_service_booking_balances, name='get_service_booking_balances'),
    url(r'^get_current_driver/(?P<vehicle_id>\d+)/$', views.get_current_driver, name='get_current_driver'),
    
    url(r'^new_vehicle_make/$', views.new_vehicle_make, name='new_vehicle_make'),   
    url(r'^new_vehicle_model/$', views.new_vehicle_model, name='new_vehicle_model'),
    url(r'^vehicles/$', views.vehicles, name='vehicles'),
    url(r'^vehicle/uploads$', views.vehicle_uploads, name='vehicle_uploads'),
    url(r'^vehicle/mileage_uploads$', views.mileage_uploads, name='mileage_uploads'),
    url(r'^vehicle/additional_vehicle_information_uploads$', views.additional_vehicle_information_uploads, name='additional_vehicle_information_uploads'),
    url(r'^vehicle/vehicle_service_due$', views.vehicle_service_due, name='vehicle_service_due'),      
    url(r'^vehicles/edit/(?P<vehicle_id>\d+)/$', views.edit_vehicle, name='edit_vehicle'),
    url(r'^vehicles/dashboard/(?P<vehicle_id>\-{0,1}\d+$)', views.vehicle_dashboard, name='vehicle_dashboard'), 
    url(r'^vehicles/purchase_detail/(?P<vehicle_id>\d+)/$', views._load_new_purchase_detail, name='_load_purchase_detail'),
    url(r'^vehicles/add/$', views.edit_vehicle, name='add_vehicle'),
    url(r'^assign_driver/(?P<vehicle_id>\d+)/$', views.assign_driver, name='assign_driver'),
    url(r'^authorize_assigned_driver/(?P<vehicle_id>\d+)/$', views.authorize_assigned_driver, name='authorize_assigned_driver'),
    url(r'^vehicles/summary/(?P<vehicle_id>\-{0,1}\d+$)', views.vehicle_summary, name='vehicle_summary'),
    
    url(r'^fuel_card_admin/$', views.fuel_card_usage, name='fuel_card_usage'),
    url(r'^fuel_card_usage/detail/(?P<fuel_card_id>(\d+))/$',views.detail_fuel_card_usage,name='detail_fuel_card_usage'),
    url(r'^fuel_card_usage/edit/(?P<fuel_card_id>\d+)/$', views.edit_fuel_card_usage, name='edit_fuel_card_usage'),
    url(r'^fuel_card_usage/add/$', views.edit_fuel_card_usage, name='add_fuel_card_usage'),
    url(r'^fuel_card_usage/uploads$', views.fuel_card_uploads, name='fuel_card_uploads'),
    url(r'^fuel_card/edit/(?P<fuel_card_id>\d+)/$', views.edit_fuel_card, name='edit_fuel_card'),
    url(r'^fuel_card/add/$', views.edit_fuel_card, name='add_fuel_card'), 
    url(r'^fuel_cards/$', views.fuel_cards, name='fuel_cards'),
    url(r'^fuel_cards/uploads$', views.fuel_cards_upload, name='fuel_cards_upload'),   

    url(r'^incidents/view/incident-details/(?P<incident_id>\-{0,1}\d+$)', views.view_incident, name='view_incident'), 
    url(r'^incidents/add/(?P<vehicle_driver_id>\-{0,1}\d+$)', views.add_incident, name='add_incident'),
    url(r'^incidents/$', views.view_incidents, name='view_incidents'),
    url(r'^incidents/add/$', views.edit_incident, name='add_incidents'),
    url(r'^incidents/edit/(?P<incident_id>\d+)/$', views.edit_incident, name='edit_incident'),
    url(r'^incident/view/(?P<incident_id>\d+)/$', views.view_incident, name='view_incident'),

    url(r'^incidents/traffic-fines/$', views.traffic_fine_list, name='view_traffic_fines'),
    url(r'^incidents/traffic-fines/add/$', views.edit_traffic_fine, name='add_traffic_fine'),
    url(r'^incidents/traffic-fines/resolve/(?P<incident_id>\d+)/$', views.resolve_fine, name='resolve_fine'),
    url(r'^incidents/traffic-fines/edit/(?P<incident_id>\d+)/$', views.edit_traffic_fine, name='edit_traffic_fine'),
    
    url(r'^document/add/(?P<vehicle_id>\-{0,1}\d+$)', views.add_document, name='add_document'),
    url(r'^document/delete/(?P<vehicle_document_id>\d+)/$', views.document_delete, name='document_delete'),
    url(r'^documents/delete/(?P<incident_document_id>\d+)/$', views.incident_document_delete, name='incident_document_delete'),

    url(r'^photo/add/(?P<vehicle_id>\-{0,1}\d+$)', views.add_photo, name='add_photo'),

    url(r'^insurers$', views.insurers, name='view_insurers'),
    url(r'^insurers/edit/(?P<insurer_id>\d+)/$', views.edit_insurer, name='edit_insurer'),
    url(r'^insurers/add/$', views.edit_insurer, name='add_insurer'),

    url(r'^insurance/vehicles/(?P<insurer_id>\-{0,1}\d+$)', views.insured, name='view_insured'),

    url(r'^documents/(?P<file_id>\d+)/$', views.file_download_task, name='file_download'),

    url(r'^vehicle_maintenance/$', views.vehicle_maintenance, name='vehicle_maintenance'),
    url(r'^vehicle_maintenance/edit/(?P<vehicle_maintenance_id>\d+)/$', views.edit_vehicle_maintenance, name='edit_vehicle_maintenance'),
    url(r'^vehicle_maintenance/add/$', views.edit_vehicle_maintenance, name='add_vehicle_maintenance'),
    url(r'^unassign_vehicle(?P<vehicle_id>\d+)/$', views.unassign_vehicle, name='unassign_vehicle'),

    url(r'^service_booking/$', views.service_booking, name='service_booking'),
    url(r'^resolved_service_booking/$', views.resolved_service_booking, name='resolved_service_booking'),
    url(r'^service_booking/edit/(?P<service_booking_id>\d+)/$', views.edit_service_booking, name='edit_service_booking'),
    url(r'^service_booking/add/$', views.edit_service_booking, name='add_service_booking'),
    url(r'^service_booking_invoice/$', views.service_booking_invoice, name='service_booking_invoice'),
    url(r'^service_booking_invoice/edit/(?P<service_booking_id>\d+)/$', views.edit_service_booking_invoice, name='edit_service_booking_invoice'),
    url(r'^service_booking_invoice/add/$', views.edit_service_booking_invoice, name='add_service_booking_invoice'),

    url(r'^service_providers$', views.vendors, name='view_vendors'),
    url(r'^service_providers/edit/(?P<vendor_id>\d+)/$', views.edit_vendor, name='edit_vendor'),
    url(r'^service_providers/add/$', views.edit_vendor, name='add_vendor'),
    
    url(r'^service_providers$', views.service_providers, name='view_service_providers'),
    url(r'^service_providers/edit/(?P<service_provider_id>\d+)/$', views.edit_service_provider, name='edit_service_provider'),
    url(r'^service_providers/add/$', views.edit_service_provider, name='add_service_provider'),
    
    url(r'^vehicle_makes$', views.vehicle_makes, name='view_vehicle_makes'),
    url(r'^vehicle_makes/edit/(?P<make_id>\d+)/$', views.edit_vehicle_make, name='edit_vehicle_make'),
    url(r'^vehicle_makes/add/$', views.edit_vehicle_make, name='add_vehicle_make'),

    url(r'^vehicle_models$', views.vehicle_models, name='view_vehicle_models'),
    url(r'^vehicle_models/edit/(?P<make_id>\d+)/(?P<model_id>\d+)/$', views.edit_vehicle_model, name='edit_vehicle_model'),
    url(r'^vehicle_models/add/$', views.edit_vehicle_model, name='add_vehicle_model'),
    url(r'^vehicle_models/add/(?P<make_id>\d+)/$', views.edit_vehicle_model, name='add_model_vehicle_make'),


    url(r'^unassign_vehicle/edit/(?P<vehicle_id>\d+)/$', views.unassign, name='unassign'),
    url(r'^unassign_fuel_card/(?P<fuel_card_id>\d+)/$', views.unassign_fuel_card, name='unassign_fuel_card'),

    url(r'^insurance_claims$', views.insurance_claims, name='view_insurance_claims'),
    url(r'^insurance_claim/edit/(?P<insurance_claim_id>\d+)/$', views.edit_insurance_claim, name='edit_insurance_claim'),
    url(r'^insurance_claim/add/$', views.edit_insurance_claim, name='add_insurance_claim'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



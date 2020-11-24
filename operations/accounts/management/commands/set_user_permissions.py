from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Set Group Permissions'

    def handle(self, *args, **kwargs):
        #do stuff

        Permission.objects.all().delete()        
          
        fleet_models = ['FileUpload', 'FuelAllocation', 'FuelCard', 'Incident', 'InsuranceClaim', 'MileageLog', 'RenewLicenceDisk', 'ServiceBooking',
                       'Trafficfine', 'Trip', 'TripLog', 'Vehicle', 'VehicleAllocation', 'VehicleExtras', 'VehicleMaintenance', 'VehicleMakeAndModel', 'Comment','Requisition',
                       'RequisitionItem', 'FuelTransfer']

        offices_models = ['Branch', 'Document', 'ElectricityMeterNumber', 'ElectricityPurchase', 'Floor', 'MobilePurchase', 'Region', 'Section',
                         'TelcomPABXContract', 'TelcomPABXContractRenewal']

        propfac_models = ['PFDocument', 'LeaseAgreement', 'LeaseAgreementRenewal', 'PFComment', 'PFRequisition', 
                         'PFRequisitionItem', 'PropertyMaintenance','OfficeInspection', 'ToiletInspection',]

        stock_models = ['STComment', 'STDocument', 'StockItem', 'StockReplenishment', 'StockTake', 'STRequisition', 
                      'STRequisitionItem', 'BranchStock',]


        model_list = {'fleet':fleet_models, 'offices':offices_models, 'propfac':propfac_models, 'stock':stock_models }
        p_types = ['view', 'create', 'edit', 'authorize']    
        for app, models in model_list.items():
            for m in models:
                print app,m
                content_type = ContentType.objects.get_or_create(app_label=app, model=m)[0]
                for p_type in p_types:
                    Permission.objects.get_or_create(codename='%s_%s' % (p_type, m.lower()),
                                                     name='%s %s' % (p_type.upper(), m),
                                                     content_type=content_type)

        content_type = ContentType.objects.get_or_create(app_label="fleet", model=m)[0]
        Permission.objects.get_or_create(codename='view_reports', name='View Reports', content_type=content_type)
        Permission.objects.get_or_create(codename='send_sms', name='Send SMS', content_type=content_type)

        ops_executive, exists = Group.objects.get_or_create(name='Operations Executive')
        ops_manager, exists = Group.objects.get_or_create(name='Operations Manager')
        ops_fleet, exists = Group.objects.get_or_create(name='Operations Fleet') 
        ops_assistant, exists = Group.objects.get_or_create(name='Operations Assistant')
        ops_assets, exists = Group.objects.get_or_create(name='Operations Assets')
        ops_stock, exists = Group.objects.get_or_create(name='Operations Stock')
        ops_offices, exists = Group.objects.get_or_create(name='Operations Offices')
        ops_property, exists = Group.objects.get_or_create(name='Operations Property And Facilities')


        r_perms = Permission.objects.filter(codename='view_reports').values_list('id', flat=True)
        for perm in r_perms:
            ops_executive.permissions.add(perm) 
            ops_manager.permissions.add(perm)
        s_perms = Permission.objects.filter(codename='send_sms').values_list('id', flat=True)
        for perm in s_perms:
            ops_executive.permissions.add(perm)
            ops_manager.permissions.add(perm)
            ops_fleet.permissions.add(perm)
            ops_assistant.permissions.add(perm) 
            ops_assets.permissions.add(perm)
            ops_stock.permissions.add(perm)
            ops_offices.permissions.add(perm)
            ops_property.permissions.add(perm) 

        #Operations Executive (Fleet)
        ops_executive.permissions.add(Permission.objects.get(codename='view_fileupload').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_fileupload').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_fileupload').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_fileupload').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_fuelallocation').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_fuelallocation').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='edit_fuelallocation').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_fuelallocation').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_fueltransfer').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_fueltransfer').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='edit_fueltransfer').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_fueltransfer').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_fuelcard').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_fuelcard').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_fuelcard').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_fuelcard').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_incident').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_incident').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_incident').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_incident').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_insuranceclaim').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_insuranceclaim').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_insuranceclaim').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_insuranceclaim').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_mileagelog').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_mileagelog').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_mileagelog').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_mileagelog').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_renewlicencedisk').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_renewlicencedisk').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_renewlicencedisk').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_renewlicencedisk').pk) 

        ops_executive.permissions.add(Permission.objects.get(codename='view_servicebooking').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_servicebooking').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_servicebooking').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_servicebooking').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_trafficfine').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_trafficfine').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_trafficfine').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_trafficfine').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_trip').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_trip').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_trip').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_trip').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_triplog').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_triplog').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_triplog').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_triplog').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_vehicle').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_vehicle').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_vehicle').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_vehicle').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_vehicleallocation').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_vehicleallocation').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_vehicleallocation').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_vehicleallocation').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_vehiclemaintenance').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_vehiclemaintenance').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_vehiclemaintenance').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_vehiclemaintenance').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_comment').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_comment').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_comment').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_comment').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_requisition').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_requisition').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_requisition').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_requisition').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_requisitionitem').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_requisitionitem').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_requisitionitem').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_requisitionitem').pk)

        #Operations Executive (Offices)
        ops_executive.permissions.add(Permission.objects.get(codename='view_telcompabxcontractrenewal').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_telcompabxcontractrenewal').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_telcompabxcontractrenewal').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_telcompabxcontractrenewal').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_telcompabxcontract').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_telcompabxcontract').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_telcompabxcontract').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_telcompabxcontract').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_section').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_section').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_section').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_section').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_region').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_region').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_region').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_region').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_mobilepurchase').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_mobilepurchase').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_mobilepurchase').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_mobilepurchase').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_floor').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_floor').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_floor').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_floor').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_electricitypurchase').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_electricitypurchase').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_electricitypurchase').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_electricitypurchase').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_electricitymeternumber').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_electricitymeternumber').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_electricitymeternumber').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_electricitymeternumber').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_document').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_document').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_document').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_document').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_branch').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_branch').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_branch').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_branch').pk)

        # Operations Executive (propfac)
        ops_executive.permissions.add(Permission.objects.get(codename='view_toiletinspection').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_toiletinspection').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_toiletinspection').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_toiletinspection').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_officeinspection').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_officeinspection').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_officeinspection').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_officeinspection').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_propertymaintenance').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_propertymaintenance').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_propertymaintenance').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_propertymaintenance').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_pfrequisitionitem').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_pfrequisitionitem').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_pfrequisitionitem').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_pfrequisitionitem').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_pfrequisition').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_pfrequisition').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_pfrequisition').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_pfrequisition').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_pfcomment').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_pfcomment').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_pfcomment').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_pfcomment').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_leaseagreementrenewal').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_leaseagreementrenewal').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_leaseagreementrenewal').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_leaseagreementrenewal').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_leaseagreement').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_leaseagreement').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_leaseagreement').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_leaseagreement').pk)

        # Operations Executive (stock)
        ops_executive.permissions.add(Permission.objects.get(codename='view_stcomment').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_stcomment').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_stcomment').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_stcomment').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_stdocument').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_stdocument').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_stdocument').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_stdocument').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_stockitem').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_stockitem').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_stockitem').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_stockitem').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_stockreplenishment').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_stockreplenishment').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_stockreplenishment').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_stockreplenishment').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_stocktake').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_stocktake').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_stocktake').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_stocktake').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_strequisition').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_strequisition').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_strequisition').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_strequisition').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_strequisitionitem').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_strequisitionitem').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_strequisitionitem').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_strequisitionitem').pk)

        ops_executive.permissions.add(Permission.objects.get(codename='view_branchstock').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='create_branchstock').pk) 
        ops_executive.permissions.add(Permission.objects.get(codename='edit_branchstock').pk)
        ops_executive.permissions.add(Permission.objects.get(codename='authorize_branchstock').pk)



        #Operations Manager (fleet)
        ops_manager.permissions.add(Permission.objects.get(codename='view_fileupload').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_fileupload').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_fileupload').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_fuelallocation').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_fuelallocation').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='edit_fuelallocation').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_fueltransfer').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_fueltransfer').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='edit_fueltransfer').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_fuelcard').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_fuelcard').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_fuelcard').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_incident').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_incident').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_incident').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_insuranceclaim').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_insuranceclaim').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_insuranceclaim').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_mileagelog').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_mileagelog').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_mileagelog').pk) 

        ops_manager.permissions.add(Permission.objects.get(codename='view_renewlicencedisk').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_renewlicencedisk').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_renewlicencedisk').pk) 

        ops_manager.permissions.add(Permission.objects.get(codename='view_servicebooking').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_servicebooking').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_servicebooking').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_trafficfine').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_trafficfine').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_trafficfine').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_trip').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_trip').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_trip').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_triplog').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_triplog').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_triplog').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_vehicle').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_vehicle').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_vehicle').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_vehicleallocation').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_vehicleallocation').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_vehicleallocation').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_vehiclemaintenance').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_vehiclemaintenance').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_vehiclemaintenance').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_comment').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_comment').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_comment').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_requisition').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_requisition').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_requisition').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_requisitionitem').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_requisitionitem').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_requisitionitem').pk)

        # Operations Manager (Offices)
        ops_manager.permissions.add(Permission.objects.get(codename='view_telcompabxcontractrenewal').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_telcompabxcontractrenewal').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_telcompabxcontractrenewal').pk)       

        ops_manager.permissions.add(Permission.objects.get(codename='view_telcompabxcontract').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_telcompabxcontract').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_telcompabxcontract').pk)
        
        ops_manager.permissions.add(Permission.objects.get(codename='view_section').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_section').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_section').pk)     

        ops_manager.permissions.add(Permission.objects.get(codename='view_region').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_region').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_region').pk)      

        ops_manager.permissions.add(Permission.objects.get(codename='view_mobilepurchase').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_mobilepurchase').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_mobilepurchase').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_floor').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_floor').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_floor').pk)       

        ops_manager.permissions.add(Permission.objects.get(codename='view_electricitypurchase').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_electricitypurchase').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_electricitypurchase').pk)     

        ops_manager.permissions.add(Permission.objects.get(codename='view_electricitymeternumber').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_electricitymeternumber').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_electricitymeternumber').pk)      

        ops_manager.permissions.add(Permission.objects.get(codename='view_document').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_document').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_document').pk)        

        ops_manager.permissions.add(Permission.objects.get(codename='view_branch').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_branch').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_branch').pk)

        # Operations Manager (propfac)
        ops_manager.permissions.add(Permission.objects.get(codename='view_toiletinspection').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_toiletinspection').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_toiletinspection').pk)        

        ops_manager.permissions.add(Permission.objects.get(codename='view_officeinspection').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_officeinspection').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_officeinspection').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_propertymaintenance').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_propertymaintenance').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_propertymaintenance').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_pfrequisitionitem').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_pfrequisitionitem').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_pfrequisitionitem').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_pfrequisition').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_pfrequisition').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_pfrequisition').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_pfcomment').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_pfcomment').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_pfcomment').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_leaseagreementrenewal').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_leaseagreementrenewal').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_leaseagreementrenewal').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_leaseagreement').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_leaseagreement').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_leaseagreement').pk)

        # Operations Manager (stock)
        ops_manager.permissions.add(Permission.objects.get(codename='view_stcomment').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_stcomment').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_stcomment').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_stdocument').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_stdocument').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_stdocument').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_stockitem').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_stockitem').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_stockitem').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_stockreplenishment').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_stockreplenishment').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_stockreplenishment').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_stocktake').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_stocktake').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_stocktake').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_strequisition').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_strequisition').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_strequisition').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_strequisitionitem').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_strequisitionitem').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_strequisitionitem').pk)

        ops_manager.permissions.add(Permission.objects.get(codename='view_branchstock').pk)
        ops_manager.permissions.add(Permission.objects.get(codename='create_branchstock').pk) 
        ops_manager.permissions.add(Permission.objects.get(codename='edit_branchstock').pk)



        #Operations Fleet (Fleet)
        ops_fleet.permissions.add(Permission.objects.get(codename='view_fileupload').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_fileupload').pk)

        ops_fleet.permissions.add(Permission.objects.get(codename='view_fuelallocation').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_fuelallocation').pk)

        ops_fleet.permissions.add(Permission.objects.get(codename='view_fueltransfer').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_fueltransfer').pk)

        ops_fleet.permissions.add(Permission.objects.get(codename='view_fuelcard').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_fuelcard').pk) 

        ops_fleet.permissions.add(Permission.objects.get(codename='view_incident').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_incident').pk)

        ops_fleet.permissions.add(Permission.objects.get(codename='view_insuranceclaim').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_insuranceclaim').pk)

        ops_fleet.permissions.add(Permission.objects.get(codename='view_mileagelog').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_mileagelog').pk) 

        ops_fleet.permissions.add(Permission.objects.get(codename='view_renewlicencedisk').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_renewlicencedisk').pk)

        ops_fleet.permissions.add(Permission.objects.get(codename='view_servicebooking').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_servicebooking').pk)

        ops_fleet.permissions.add(Permission.objects.get(codename='view_trafficfine').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_trafficfine').pk)

        ops_fleet.permissions.add(Permission.objects.get(codename='view_trip').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_trip').pk)

        ops_fleet.permissions.add(Permission.objects.get(codename='view_triplog').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_triplog').pk) 

        ops_fleet.permissions.add(Permission.objects.get(codename='view_vehicle').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_vehicle').pk) 

        ops_fleet.permissions.add(Permission.objects.get(codename='view_vehicleallocation').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_vehicleallocation').pk)


        ops_fleet.permissions.add(Permission.objects.get(codename='view_vehiclemaintenance').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_vehiclemaintenance').pk)

        ops_fleet.permissions.add(Permission.objects.get(codename='view_comment').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_comment').pk) 


        ops_fleet.permissions.add(Permission.objects.get(codename='view_requisition').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_requisition').pk) 


        ops_fleet.permissions.add(Permission.objects.get(codename='view_requisitionitem').pk)
        ops_fleet.permissions.add(Permission.objects.get(codename='create_requisitionitem').pk)



        #Operations Assistant (Fleet)
        ops_assistant.permissions.add(Permission.objects.get(codename='view_fileupload').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_fileupload').pk)


        ops_assistant.permissions.add(Permission.objects.get(codename='view_fuelallocation').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_fuelallocation').pk)

        ops_assistant.permissions.add(Permission.objects.get(codename='view_fueltransfer').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_fueltransfer').pk)


        ops_assistant.permissions.add(Permission.objects.get(codename='view_fuelcard').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_fuelcard').pk) 


        ops_assistant.permissions.add(Permission.objects.get(codename='view_incident').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_incident').pk) 


        ops_assistant.permissions.add(Permission.objects.get(codename='view_insuranceclaim').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_insuranceclaim').pk)


        ops_assistant.permissions.add(Permission.objects.get(codename='view_mileagelog').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_mileagelog').pk) 


        ops_assistant.permissions.add(Permission.objects.get(codename='view_renewlicencedisk').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_renewlicencedisk').pk)


        ops_assistant.permissions.add(Permission.objects.get(codename='view_servicebooking').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_servicebooking').pk) 


        ops_assistant.permissions.add(Permission.objects.get(codename='view_trafficfine').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_trafficfine').pk) 


        ops_assistant.permissions.add(Permission.objects.get(codename='view_trip').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_trip').pk) 


        ops_assistant.permissions.add(Permission.objects.get(codename='view_triplog').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_triplog').pk) 


        ops_assistant.permissions.add(Permission.objects.get(codename='view_vehicle').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_vehicle').pk) 


        ops_assistant.permissions.add(Permission.objects.get(codename='view_vehicleallocation').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_vehicleallocation').pk)


        ops_assistant.permissions.add(Permission.objects.get(codename='view_vehiclemaintenance').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_vehiclemaintenance').pk) 


        ops_assistant.permissions.add(Permission.objects.get(codename='view_comment').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_comment').pk) 


        ops_assistant.permissions.add(Permission.objects.get(codename='view_requisition').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_requisition').pk) 


        ops_assistant.permissions.add(Permission.objects.get(codename='view_requisitionitem').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_requisitionitem').pk)

        # Operations Assistant (Offices)
        ops_assistant.permissions.add(Permission.objects.get(codename='view_telcompabxcontractrenewal').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_telcompabxcontractrenewal').pk) 

        ops_assistant.permissions.add(Permission.objects.get(codename='view_telcompabxcontract').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_telcompabxcontract').pk)
        
        ops_assistant.permissions.add(Permission.objects.get(codename='view_section').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_section').pk)     

        ops_assistant.permissions.add(Permission.objects.get(codename='view_region').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_region').pk)  

        ops_assistant.permissions.add(Permission.objects.get(codename='view_mobilepurchase').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_mobilepurchase').pk)

        ops_assistant.permissions.add(Permission.objects.get(codename='view_floor').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_floor').pk)

        ops_assistant.permissions.add(Permission.objects.get(codename='view_electricitypurchase').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_electricitypurchase').pk) 

        ops_assistant.permissions.add(Permission.objects.get(codename='view_electricitymeternumber').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_electricitymeternumber').pk)  

        ops_assistant.permissions.add(Permission.objects.get(codename='view_document').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_document').pk)    

        ops_assistant.permissions.add(Permission.objects.get(codename='view_branch').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_branch').pk) 


        # Operations Assistant (propfac)
        ops_assistant.permissions.add(Permission.objects.get(codename='view_toiletinspection').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_toiletinspection').pk)    

        ops_assistant.permissions.add(Permission.objects.get(codename='view_officeinspection').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_officeinspection').pk)

        ops_assistant.permissions.add(Permission.objects.get(codename='view_propertymaintenance').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_propertymaintenance').pk)

        ops_assistant.permissions.add(Permission.objects.get(codename='view_pfrequisitionitem').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_pfrequisitionitem').pk) 

        ops_assistant.permissions.add(Permission.objects.get(codename='view_pfrequisition').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_pfrequisition').pk)

        ops_assistant.permissions.add(Permission.objects.get(codename='view_pfcomment').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_pfcomment').pk)

        ops_assistant.permissions.add(Permission.objects.get(codename='view_leaseagreementrenewal').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_leaseagreementrenewal').pk) 

        ops_assistant.permissions.add(Permission.objects.get(codename='view_leaseagreement').pk)
        ops_assistant.permissions.add(Permission.objects.get(codename='create_leaseagreement').pk)



        # Operations Offices (Offices)
        ops_offices.permissions.add(Permission.objects.get(codename='view_telcompabxcontractrenewal').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_telcompabxcontractrenewal').pk) 

        ops_offices.permissions.add(Permission.objects.get(codename='view_telcompabxcontract').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_telcompabxcontract').pk)
        
        ops_offices.permissions.add(Permission.objects.get(codename='view_section').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_section').pk)   

        ops_offices.permissions.add(Permission.objects.get(codename='view_region').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_region').pk)

        ops_offices.permissions.add(Permission.objects.get(codename='view_mobilepurchase').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_mobilepurchase').pk)

        ops_offices.permissions.add(Permission.objects.get(codename='view_floor').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_floor').pk) 

        ops_offices.permissions.add(Permission.objects.get(codename='view_electricitypurchase').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_electricitypurchase').pk) 

        ops_offices.permissions.add(Permission.objects.get(codename='view_electricitymeternumber').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_electricitymeternumber').pk) 

        ops_offices.permissions.add(Permission.objects.get(codename='view_document').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_document').pk) 

        ops_offices.permissions.add(Permission.objects.get(codename='view_branch').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_branch').pk)

        # Operations Offices (propfac)
        ops_offices.permissions.add(Permission.objects.get(codename='view_toiletinspection').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_toiletinspection').pk)  

        ops_offices.permissions.add(Permission.objects.get(codename='view_officeinspection').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_officeinspection').pk)

        ops_offices.permissions.add(Permission.objects.get(codename='view_propertymaintenance').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_propertymaintenance').pk)

        ops_offices.permissions.add(Permission.objects.get(codename='view_pfrequisitionitem').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_pfrequisitionitem').pk)

        ops_offices.permissions.add(Permission.objects.get(codename='view_pfrequisition').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_pfrequisition').pk) 

        ops_offices.permissions.add(Permission.objects.get(codename='view_pfcomment').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_pfcomment').pk)

        ops_offices.permissions.add(Permission.objects.get(codename='view_leaseagreementrenewal').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_leaseagreementrenewal').pk)

        ops_offices.permissions.add(Permission.objects.get(codename='view_leaseagreement').pk)
        ops_offices.permissions.add(Permission.objects.get(codename='create_leaseagreement').pk) 



        # Operations Property And Facilities (Offices)
        ops_property.permissions.add(Permission.objects.get(codename='view_telcompabxcontractrenewal').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_telcompabxcontractrenewal').pk) 

        ops_property.permissions.add(Permission.objects.get(codename='view_telcompabxcontract').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_telcompabxcontract').pk)
        
        ops_property.permissions.add(Permission.objects.get(codename='view_section').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_section').pk)  

        ops_property.permissions.add(Permission.objects.get(codename='view_region').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_region').pk) 

        ops_property.permissions.add(Permission.objects.get(codename='view_mobilepurchase').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_mobilepurchase').pk)

        ops_property.permissions.add(Permission.objects.get(codename='view_floor').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_floor').pk) 

        ops_property.permissions.add(Permission.objects.get(codename='view_electricitypurchase').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_electricitypurchase').pk)  

        ops_property.permissions.add(Permission.objects.get(codename='view_electricitymeternumber').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_electricitymeternumber').pk)

        ops_property.permissions.add(Permission.objects.get(codename='view_document').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_document').pk)     

        ops_property.permissions.add(Permission.objects.get(codename='view_branch').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_branch').pk)


        # Operations Property And Facilities (propfac)
        ops_property.permissions.add(Permission.objects.get(codename='view_toiletinspection').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_toiletinspection').pk) 

        ops_property.permissions.add(Permission.objects.get(codename='view_officeinspection').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_officeinspection').pk) 
        ops_property.permissions.add(Permission.objects.get(codename='edit_officeinspection').pk)

        ops_property.permissions.add(Permission.objects.get(codename='view_propertymaintenance').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_propertymaintenance').pk) 

        ops_property.permissions.add(Permission.objects.get(codename='view_pfrequisitionitem').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_pfrequisitionitem').pk)

        ops_property.permissions.add(Permission.objects.get(codename='view_pfrequisition').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_pfrequisition').pk)

        ops_property.permissions.add(Permission.objects.get(codename='view_pfcomment').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_pfcomment').pk)

        ops_property.permissions.add(Permission.objects.get(codename='view_leaseagreementrenewal').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_leaseagreementrenewal').pk) 

        ops_property.permissions.add(Permission.objects.get(codename='view_leaseagreement').pk)
        ops_property.permissions.add(Permission.objects.get(codename='create_leaseagreement').pk)


        # Operations assets
        ops_assets.permissions.add(Permission.objects.get(codename='view_stcomment').pk)
        ops_assets.permissions.add(Permission.objects.get(codename='create_stcomment').pk)

        ops_assets.permissions.add(Permission.objects.get(codename='view_stdocument').pk)
        ops_assets.permissions.add(Permission.objects.get(codename='create_stdocument').pk)

        ops_assets.permissions.add(Permission.objects.get(codename='view_stockitem').pk)
        ops_assets.permissions.add(Permission.objects.get(codename='create_stockitem').pk)

        ops_assets.permissions.add(Permission.objects.get(codename='view_stockreplenishment').pk)
        ops_assets.permissions.add(Permission.objects.get(codename='create_stockreplenishment').pk)

        ops_assets.permissions.add(Permission.objects.get(codename='view_stocktake').pk)
        ops_assets.permissions.add(Permission.objects.get(codename='create_stocktake').pk)

        ops_assets.permissions.add(Permission.objects.get(codename='view_strequisition').pk)
        ops_assets.permissions.add(Permission.objects.get(codename='create_strequisition').pk)

        ops_assets.permissions.add(Permission.objects.get(codename='view_strequisitionitem').pk)
        ops_assets.permissions.add(Permission.objects.get(codename='create_strequisitionitem').pk)

        ops_assets.permissions.add(Permission.objects.get(codename='view_branchstock').pk)
        ops_assets.permissions.add(Permission.objects.get(codename='create_branchstock').pk)


        # Operations stock
        ops_stock.permissions.add(Permission.objects.get(codename='view_stcomment').pk)
        ops_stock.permissions.add(Permission.objects.get(codename='create_stcomment').pk)

        ops_stock.permissions.add(Permission.objects.get(codename='view_stdocument').pk)
        ops_stock.permissions.add(Permission.objects.get(codename='create_stdocument').pk)

        ops_stock.permissions.add(Permission.objects.get(codename='view_stockitem').pk)
        ops_stock.permissions.add(Permission.objects.get(codename='create_stockitem').pk) 

        ops_stock.permissions.add(Permission.objects.get(codename='view_stockreplenishment').pk)
        ops_stock.permissions.add(Permission.objects.get(codename='create_stockreplenishment').pk)

        ops_stock.permissions.add(Permission.objects.get(codename='view_stocktake').pk)
        ops_stock.permissions.add(Permission.objects.get(codename='create_stocktake').pk)

        ops_stock.permissions.add(Permission.objects.get(codename='view_strequisition').pk)
        ops_stock.permissions.add(Permission.objects.get(codename='create_strequisition').pk)

        ops_stock.permissions.add(Permission.objects.get(codename='view_strequisitionitem').pk)
        ops_stock.permissions.add(Permission.objects.get(codename='create_strequisitionitem').pk)

        ops_stock.permissions.add(Permission.objects.get(codename='view_branchstock').pk)
        ops_stock.permissions.add(Permission.objects.get(codename='create_branchstock').pk)
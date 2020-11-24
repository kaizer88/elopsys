from django.conf.urls import url, handler400, handler403, handler404, handler500
from . import views
from propfac.models import *


handler400 = 'fleet.views.handler400'
handler403 = 'fleet.views.handler403'
handler404 = 'fleet.views.handler404'
handler500 = 'fleet.views.handler500'

urlpatterns = [    
   
    
    url(r'^stock/view/stocklist/$', views.stockItemsList, name='stockitems_list'),   
    url(r'^stock/add/stockitem/$', views.addStockItem, name='add_stockitem'),
    url(r'^stock/edit/stockitem/(?P<obj_id>\-{0,1}\d+$)', views.editStockItem, name='edit_stockitem'),

    url(r'^stock/add/branch/stockitem/(?P<obj_id>\-{0,1}\d+$)', views.branchStockItem, name='add_branchstockitem'),
    url(r'^stock/edit/branch/stockitem/(?P<obj_id>\-{0,1}\d+$)', views.editBranchStockItem, name='edit_branchstockitem'), 

    url(r'^stock/add/book/$', views.applicationBooks, name='add_applicationbook'),
    url(r'^stock/add/bookreplenishment/(?P<obj_id>\-{0,1}\d+$)', views.bookReplenishment, name='add_bookreplenishment'),  

    # url(r'^stock/add/stockitem/replenishment/(?P<obj_id>\-{0,1}\d+$)', views.stockItemReplenishment, name='add_stockitemreplenishment'),
    url(r'^stock/add/stockitem/replenishment/(?P<obj_id>\-{0,1}\d+$)', views.stockItemReplenishment, name='add_stockitemreplenishment'),
    url(r'^stock/add/stockitems/replenishment/(?P<obj_id>\-{0,1}\d+$)', views.stockItemsReplenishment, name='add_stockreplenishment'),
    url(r'^stock/edit/stockitem/replenishment/(?P<obj_id>\-{0,1}\d+$)', views.editStockItemReplenishment, name='edit_stockitemreplenishment'),
    url(r'^stock/view/stockreplenishmentlist/$', views.stockReplenishmentList, name='stockreplenishment_list'), 

    url(r'^stock/add/stocktake(?P<obj_id>\-{0,1}\d+$)', views.stockTake, name='add_stocktake'),
    url(r'^stock/stocktaking(?P<obj_id>\-{0,1}\d+$)', views.stockTaking, name='add_stocktaking'),
    url(r'^stock/edit/stocktake(?P<obj_id>\-{0,1}\d+$)', views.editStockTake, name='edit_stocktake'),
    url(r'^stock/view/stocktakelist/$', views.stockTakeList, name='stocktake_list'), 

    # url(r'^property/renew/leaseagreement/(?P<obj_id>\-{0,1}\d+$)', views.renewLeaseAgreement, name='renew_leaseagreement'),
    # url(r'^property/edit/renew/leaseagreement/(?P<obj_id>\-{0,1}\d+$)', views.editLeaseAgreementRenwal, name='edit_renew_leaseagreement'),

    # url(r'^property/add/inspection/(?P<obj_id>\-{0,1}\d+$)', views.officeInspection, name='add_officeinspection'),
    # url(r'^property/edit/inspection/(?P<obj_id>\-{0,1}\d+$)', views.editOfficeInspection, name='edit_officeinspection'),
    # url(r'^property/add/toiletinspection/(?P<obj_id>\-{0,1}\d+$)', views.officeToiletInspection, name='add_officetoiletinspection'),
    # url(r'^property/edit/toiletinspection/(?P<obj_id>\-{0,1}\d+$)', views.editOfficeToiletInspection, name='edit_officetoiletinspection'),
    # url(r'^property/view/inspection/list/$', views.inspectionsList, name='inspections_list'), 

    # url(r'^property/add/maintenance/(?P<obj_id>\-{0,1}\d+$)', views.propertyMaintenance, name='add_propertymaintenance'),
    # url(r'^property/edit/maintenance/(?P<obj_id>\-{0,1}\d+$)', views.editPropertyMaintenance, name='edit_propertymaintanance'),
    # url(r'^property/view/maintenance/list/$', views.propertyMaintenanceList, name='propertymaintenance_list'),

    # url(r'^property/add/mobilepurchase/(?P<obj_id>\-{0,1}\d+$)', views.mobilePurchase, name='add_mobilepurchase'),
    # url(r'^property/edit/mobilepurchase/(?P<obj_id>\-{0,1}\d+$)', views.editMobilePurchase, name='edit_mobilepurchase'),
    # url(r'^property/view/mobilepurchases/list/$', views.mobilePurchaseList, name='mobilepurchases_list'),

    # url(r'^property/add/electricitypurchase/(?P<obj_id>\-{0,1}\d+$)', views.electricityPurchase, name='add_electricitypurchase'),
    # url(r'^property/edit/electricitypurchase/(?P<obj_id>\-{0,1}\d+$)', views.editElectricityPurchase, name='edit_electricitypurchase'),
    # url(r'^property/view/electricitypurchase/list/$', views.electricityPurchaseList, name='electricitypurchases_list'),

    # url(r'^property/add/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.telcomPABXContract, name='add_telcomcontract'),
    # url(r'^property/edit/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.editTelcomPABXContract, name='edit_telcomcontract'),
    # url(r'^property/view/telcomcontract/list/$', views.telcomPABXContractList, name='telcomcontracts_list'),

    # url(r'^property/renew/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.telcomPABXContractRenewal, name='add_telcomcontractrenewal'),
    # url(r'^property/edit/renew/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.editTelcomPABXContractRenewal, name='edit_telcomcontractrenewal'),   
    
    # url(r'^property/requisition/propertymaintenance/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':PropertyMaintenance}, name='requisition_propertymaintenance'),
    # url(r'^property/requisition/renewal/leaseagreement/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':LeaseAgreementRenewal}, name='requisition_leaseagreement_renewal'),
    # url(r'^property/requisition/new/leaseagreement/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':LeaseAgreement}, name='requisition_leaseagreement'),
    # url(r'^property/requisition/new/mobilepurchase/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':MobilePurchase}, name='requisition_mobilepurchase'),
    # url(r'^property/requisition/new/electricitypurchase/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':ElectricityPurchase}, name='requisition_electricitypurchase'),
    # url(r'^property/requisition/new/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':TelcomPABXContract}, name='requisition_telcomcontract'),
    # url(r'^property/requisition/renew/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':TelcomPABXContractRenewal}, name='requisition_telcomcontractrenewal'),

    # url(r'^property/requisition/item/(?P<obj_id>\-{0,1}\d+$)', views.requisition_item, name='requisition_item'),
    # url(r'^property/view/requisition/(?P<obj_id>\-{0,1}\d+$)', views.view_requisition, name='view_requisition'),
    
   
   
    
    ]

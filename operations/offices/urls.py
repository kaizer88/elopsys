from django.conf.urls import url, handler400, handler403, handler404, handler500
from . import views
from offices.models import *


handler400 = 'fleet.views.handler400'
handler403 = 'fleet.views.handler403'
handler404 = 'fleet.views.handler404'
handler500 = 'fleet.views.handler500'

urlpatterns = [
    
   
    # url(r'^property/view/authorizations/list/$', views.propertyAuthorizations, name='propertyauthorizations'),

    # url(r'^view/property/(?P<obj_id>\-{0,1}\d+$)', views.viewproperty, name='viewproperty'), 
    # url(r'^property/view/branch/list/$', views.branchList, name='branch_list'),   
    # url(r'^property/add/leaseagreement/(?P<obj_id>\-{0,1}\d+$)', views.addLeaseAgreement, name='add_leaseagreement'),
    # url(r'^property/edit/leaseagreement/(?P<obj_id>\-{0,1}\d+$)', views.editLeaseAgreement, name='edit_leaseagreement'),
    # url(r'^property/leaseagreements/list/$', views.LeaseAgreementList, name='leaseagreements_list'), 

    # url(r'^property/renew/leaseagreement/(?P<obj_id>\-{0,1}\d+$)', views.renewLeaseAgreement, name='renew_leaseagreement'),
    # url(r'^property/edit/renew/leaseagreement/(?P<obj_id>\-{0,1}\d+$)', views.editLeaseAgreementRenwal, name='edit_renew_leaseagreement'),

    url(r'^offices/mobilenumbers/$', views.mobileNumbers, name='mobilenumbers'),
    url(r'^offices/edit/mobilenumber/(?P<obj_id>\-{0,1}\d+$)', views.editMobileNumber, name='edit_mobilenumber'),
    url(r'^offices/card/allocations/$', views.cardAllocation, name='cardallocations'),
    url(r'^offices/edit/cardallocation/(?P<obj_id>\-{0,1}\d+$)', views.editCardAlloction, name='edit_cardallocation'),

    # url(r'^property/add/toiletinspection/(?P<obj_id>\-{0,1}\d+$)', views.officeToiletInspection, name='add_officetoiletinspection'),
    # url(r'^property/edit/toiletinspection/(?P<obj_id>\-{0,1}\d+$)', views.editOfficeToiletInspection, name='edit_officetoiletinspection'),
    # url(r'^property/view/inspection/list/$', views.inspectionsList, name='inspections_list'), 

    # url(r'^property/add/maintenance/(?P<obj_id>\-{0,1}\d+$)', views.propertyMaintenance, name='add_propertymaintenance'),
    # url(r'^property/edit/maintenance/(?P<obj_id>\-{0,1}\d+$)', views.editPropertyMaintenance, name='edit_propertymaintanance'),
    # url(r'^property/view/maintenance/list/$', views.propertyMaintenanceList, name='propertymaintenance_list'),

    # url(r'^offices/add/mobilepurchase/(?P<obj_id>\-{0,1}\d+$)', views.mobilePurchase, name='add_mobilepurchase'),
    # url(r'^offices/edit/mobilepurchase/(?P<obj_id>\-{0,1}\d+$)', views.editMobilePurchase, name='edit_mobilepurchase'),
    # url(r'^offices/view/mobilepurchases/list/$', views.mobilePurchaseList, name='mobilepurchases_list'),

    # url(r'^offices/add/electricitypurchase/(?P<obj_id>\-{0,1}\d+$)', views.electricityPurchase, name='add_electricitypurchase'),
    # url(r'^offices/edit/electricitypurchase/(?P<obj_id>\-{0,1}\d+$)', views.editElectricityPurchase, name='edit_electricitypurchase'),
    # url(r'^offices/view/electricitypurchase/list/$', views.electricityPurchaseList, name='electricitypurchases_list'),

    # url(r'^offices/add/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.telcomPABXContract, name='add_telcomcontract'),
    # url(r'^offices/edit/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.editTelcomPABXContract, name='edit_telcomcontract'),
    # url(r'^offices/view/telcomcontract/list/$', views.telcomPABXContractList, name='telcomcontracts_list'),

    # url(r'^offices/renew/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.telcomPABXContractRenewal, name='add_telcomcontractrenewal'),
    # url(r'^offices/edit/renew/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.editTelcomPABXContractRenewal, name='edit_telcomcontractrenewal'),   
    
    # url(r'^property/requisition/propertymaintenance/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':PropertyMaintenance}, name='requisition_propertymaintenance'),
    # url(r'^property/requisition/renewal/leaseagreement/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':LeaseAgreementRenewal}, name='requisition_leaseagreement_renewal'),
    # url(r'^property/requisition/new/leaseagreement/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':LeaseAgreement}, name='requisition_leaseagreement'),
    # url(r'^offices/requisition/new/mobilepurchase/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':MobilePurchase}, name='requisition_mobilepurchase'),
    # url(r'^offices/requisition/new/electricitypurchase/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':ElectricityPurchase}, name='requisition_electricitypurchase'),
    # url(r'^offices/requisition/new/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':TelcomPABXContract}, name='requisition_telcomcontract'),
    # url(r'^offices/requisition/renew/telcomcontract/(?P<obj_id>\-{0,1}\d+$)', views.requisition, {'obj_type':TelcomPABXContractRenewal}, name='requisition_telcomcontractrenewal'),

    # url(r'^property/requisition/item/(?P<obj_id>\-{0,1}\d+$)', views.requisition_item, name='requisition_item'),
    # url(r'^property/view/requisition/(?P<obj_id>\-{0,1}\d+$)', views.view_requisition, name='view_requisition'),
    
   

    
    ]

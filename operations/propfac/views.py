from django.shortcuts import render

# Create your views here.
from django import http
from django.template.loader import render_to_string, get_template
from django.template import RequestContext, Context
from django.conf import settings
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from datetime import datetime, timedelta, date
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from forms import *
import csv
import os
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
# from propfac.models import LeaseAgreement,LeaseAgreementRenewal, Document, LeaseAgreementRenewal, PropertyMaintenance,\
#                     OfficeInspection, PFComment, PFRequisition, PFRequisitionItem
from propfac.models import *


# from employees.models import Employee, Contact
from employees.models import *
from offices.models import *
from django.db.models import Count, Sum, Q
import collections
import json
from sms.sms_helper import *
from fleet.views import handler400,handler403, handler404, handler500

@login_required
def get_branch(request):
    term = request.GET.get('term', '')
    branches = Branch.objects.filter(branch__icontains=term).distinct()[:20]

    data = []

    for n in branches:
        branch = {}
        branch['id'] = n.id
        branch['label'] = n.branch
        branch['value'] = n.branch
        data.append(branch)       

    results = json.dumps(data)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
def get_floor(request, branch_id):   
    floors = Floor.objects.filter(branch__pk=branch_id)

    data = []

    for n in floors:
        floor = {}
        floor['id'] = n.id
        floor['label'] = n.floor
        floor['value'] = n.floor
        data.append(floor)       

    results = json.dumps(data)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
def get_section(request, floor_id): 
    sections = Section.objects.filter(floor__pk=floor_id)

    data = []

    for n in sections:
        section = {}
        section['id'] = n.id
        section['label'] = n.section_no +' '+ n.description
        section['value'] = n.id
        data.append(section)       

    results = json.dumps(data)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)





@login_required
@permission_required('offices.view_branch', raise_exception=True)
def branchList(request):
    title = "Branches List" 
    branches = Branch.objects.all().order_by('id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_branches' in request.GET and filter_form.is_valid():
        branches = filter_form.filter(branches, date)   
    page = request.GET.get('page', 1)
    branches_paginator = Paginator(branches, 14)
    try:
        branches = branches_paginator.page(page)
    except PageNotAnInteger:
        branches = branches_paginator.page(1)
    except EmptyPage:
        branches = branches_paginator.page(branches_paginator.num_pages)

    context ={
        "title": title,
        "branches": branches,        
        "filter_form": filter_form,       
        }       
    return render(request, "branchList.html", context)

@login_required
@user_passes_test(lambda u: u.is_executive or u.is_superuser)
def propertyAuthorizations(request):
    title = "Property And Facilities Authorizations"    
    property_maintenance = PropertyMaintenance.objects.all().order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_property_maintenance' in request.GET and filter_form.is_valid():
        property_maintenance = filter_form.filter(property_maintenance, date)   
    page = request.GET.get('page', 1)
    property_maintenance_paginator = Paginator(property_maintenance, 14)
    try:
        property_maintenance = property_maintenance_paginator.page(page)
    except PageNotAnInteger:
        property_maintenance = property_maintenance_paginator.page(1)
    except EmptyPage:
        property_maintenance = property_maintenance_paginator.page(property_maintenance_paginator.num_pages)

    leases = LeaseAgreement.objects.all().order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_leases' in request.GET and filter_form.is_valid():
        leases = filter_form.filter(leases, date)   
    page = request.GET.get('page', 1)
    leases_paginator = Paginator(leases, 14)
    try:
        leases = leases_paginator.page(page)
    except PageNotAnInteger:
        leases = leases_paginator.page(1)
    except EmptyPage:
        leases = leases_paginator.page(leases_paginator.num_pages)


    renewal = LeaseAgreementRenewal.objects.all().order_by('-id')
    date = 'new_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_renewal' in request.GET and filter_form.is_valid():
        renewal = filter_form.filter(renewal, date)   
    page = request.GET.get('page', 1)
    renewal_paginator = Paginator(renewal, 14)
    try:
        renewal = renewal_paginator.page(page)
    except PageNotAnInteger:
        renewal = renewal_paginator.page(1)
    except EmptyPage:
        renewal = renewal_paginator.page(renewal_paginator.num_pages)



    context ={
        "title": title,
        "property_maintenance": property_maintenance, 
        "renewal": renewal,
        "leases":leases,       
        "filter_form": filter_form,       
        }       
    return render(request, "PF_authorizations.html", context)


@login_required
@permission_required('offices.create_telcompabxcontractrenewal', raise_exception=True)
def telcomPABXContractRenewal(request, obj_id):
    title = "Telcom PABX Contract Renewal"
    
    branch = Branch.objects.get(pk=obj_id)    
    contract = TelcomPABXContractRenewal(branch = branch)

    form = TelcomPABXContractRenewalForm(request.POST or None, instance=contract, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(branch=branch, obj_type="TelcomPABXContractRenewal")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    

    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                latest_trans = TelcomPABXContractRenewal.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "TelcomPABXContractRenewal"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = latest_trans.id
                    uploaded.branch = latest_trans.branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_ype = "TelcomPABXContractRenewal"                          
                    uploaded.save()

                return HttpResponseRedirect(reverse('property:requisition_telcomcontractrenewal', kwargs={'obj_id':latest_trans.id}))               
    return render(request, "property.html", context)


@login_required
@permission_required('offices.edit_telcompabxcontractrenewal', raise_exception=True)
def editTelcomPABXContractRenewal(request, obj_id): 
    title = "Edit Telcom PABXC ontract Renewal"  
    transaction = TelcomPABXContractRenewal.objects.get(pk=obj_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    branch = transaction.branch
    branch_id = Branch.objects.filter(branch=branch)
    branch = Branch.objects.get(pk=branch_id) 
    try:
        requisition = PFRequisition.objects.get(obj_id=obj_id, requisition_type="TelcomPABXContractRenewal")
    except PFRequisition.DoesNotExist:
        requisition = None   
    uploads = PFDocument.objects.filter(branch=branch).filter(obj_type="TelcomPABXContractRenewal").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = TelcomPABXContractRenewalForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form":upload_file_form,
        "comment_form":comment_form,
        "uploads":uploads,
        "sliders":images,
        "comments":comments,
        
        }

    post = request.POST
    if request.POST:        
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = creator
                save_form.modified_by = request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)                   
                    new_comment.branch = branch
                    new_comment.comment_type = "TelcomPABXContractRenewal"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.obj_id = transaction.id
                    uploaded.branch = branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_type = "TelcomPABXContractRenewal"
                    uploaded.save() 
               
                if request.user.has_perm('authorize_telcompabxcontractrenewal'):
                    if requisition:   
                        return HttpResponseRedirect(reverse('property:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('property:propertyauthorizations'))
                else:
                    return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))     
    return render(request, "property.html", context)


@login_required
@permission_required('offices.create_telcompabxcontract', raise_exception=True)
def telcomPABXContract(request, obj_id):
    title = "Telcom PABX Contract"
    
    branch = Branch.objects.get(pk=obj_id)    
    contract = TelcomPABXContract(branch = branch)

    form = TelcomPABXContractForm(request.POST or None, instance=contract, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(branch=branch, obj_type="TelcomPABXContract")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    

    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                latest_trans = TelcomPABXContract.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "TelcomPABXContract"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = latest_trans.id
                    uploaded.branch = latest_trans.branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_ype = "TelcomPABXContract"                          
                    uploaded.save()

                return HttpResponseRedirect(reverse('property:requisition_telcomcontract', kwargs={'obj_id':latest_trans.id}))               
    return render(request, "property.html", context)

@login_required
@permission_required('offices.edit_telcompabxcontract', raise_exception=True)
def editTelcomPABXContract(request, obj_id): 
    title = "Edit Mobile Purchase"  
    transaction = TelcomPABXContract.objects.get(pk=obj_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    branch = transaction.branch
    branch_id = Branch.objects.filter(branch=branch)
    branch = Branch.objects.get(pk=branch_id) 
    try:
        requisition = PFRequisition.objects.get(obj_id=obj_id, requisition_type="TelcomPABXContract")
    except PFRequisition.DoesNotExist:
        requisition = None   
    uploads = PFDocument.objects.filter(branch=branch).filter(obj_type="TelcomPABXContract").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = TelcomPABXContractForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form":upload_file_form,
        "comment_form":comment_form,
        "uploads":uploads,
        "sliders":images,
        "comments":comments,
        
        }

    post = request.POST
    if request.POST:        
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save_form.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)                   
                    new_comment.branch = branch
                    new_comment.comment_type = "TelcomPABXContract"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.obj_id = transaction.id
                    uploaded.branch = branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_type = "TelcomPABXContract"
                    uploaded.save() 
               
                if request.user.has_perm('authorize_telcompabxcontract'):
                    if requisition:   
                        return HttpResponseRedirect(reverse('property:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('property:propertyauthorizations'))
                else:
                    return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))     
    return render(request, "property.html", context)


@login_required
@permission_required('offices.view_telcompabxcontract', raise_exception=True)
def telcomPABXContractList(request):
    title = "Telkom PABX Contracts List"    
    contracts = TelcomPABXContract.objects.all().order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_contracts' in request.GET and filter_form.is_valid():
        contracts = filter_form.filter(contracts, date)   
    page = request.GET.get('page', 1)
    contracts_paginator = Paginator(contracts, 14)
    try:
        contracts = contracts_paginator.page(page)
    except PageNotAnInteger:
        contracts = contracts_paginator.page(1)
    except EmptyPage:
        contracts = contracts_paginator.page(contracts_paginator.num_pages)

    contract_renewals = TelcomPABXContractRenewal.objects.all().order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_renewals' in request.GET and filter_form.is_valid():
        contract_renewals = filter_form.filter(contract_renewals, date)   
    page = request.GET.get('page', 1)
    contract_renewals_paginator = Paginator(contract_renewals, 14)
    try:
        contract_renewals = contract_renewals_paginator.page(page)
    except PageNotAnInteger:
        contract_renewals = contract_renewals_paginator.page(1)
    except EmptyPage:
        contract_renewals = contract_renewals_paginator.page(contract_renewals_paginator.num_pages)

    due_expiry_date = datetime.now() + timedelta(+30)
    expired_date = datetime.now() + timedelta(-1)
    todays_date = datetime.now()+ timedelta()
      
    contracts_expiring = TelcomPABXContract.objects.filter(expiry_date__range=[todays_date, due_expiry_date]).order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_expiring' in request.GET and filter_form.is_valid():
        contracts_expiring = filter_form.filter(contracts_expiring, date)   
    page = request.GET.get('page', 1)
    contracts_expiring_paginator = Paginator(contracts_expiring, 14)
    try:
        contracts_expiring = contracts_expiring_paginator.page(page)
    except PageNotAnInteger:
        contracts_expiring = contracts_expiring_paginator.page(1)
    except EmptyPage:
        contracts_expiring = contracts_expiring_paginator.page(contracts_expiring_paginator.num_pages)
   
    contracts_expired = TelcomPABXContract.objects.filter(expiry_date__lte=expired_date).order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_expired' in request.GET and filter_form.is_valid():
        contracts_expired = filter_form.filter(contracts_expired, date)   
    page = request.GET.get('page', 1)
    contracts_expired_paginator = Paginator(contracts_expired, 14)
    try:
        contracts_expired = contracts_expired_paginator.page(page)
    except PageNotAnInteger:
        contracts_expired = contracts_expired_paginator.page(1)
    except EmptyPage:
        contracts_expired = contracts_expired_paginator.page(contracts_expired_paginator.num_pages)

    context ={
        "title": title,
        "contracts": contracts,
        "contracts_expiring": contracts_expiring,
        "contracts_expired": contracts_expired,
        "contract_renewals": contract_renewals,       
        "filter_form": filter_form,       
        }       
    return render(request, "telcomPABXContractList.html", context)


@login_required
@permission_required('office.create_electricitypurchase', raise_exception=True)
def electricityPurchase(request, obj_id):
    title = "Electricity Purchase"
    
    branch = Branch.objects.get(pk=obj_id) 
    meter_number = ElectricityMeterNumber.objects.get(branch_id=branch)   
    purchase = ElectricityPurchase(meter_number=meter_number)

    form = ElectricityPurchaseForm(request.POST or None, instance=purchase, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(branch=branch, obj_type="ElectricityPurchase")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    

    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                latest_trans = ElectricityPurchase.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "ElectricityPurchase"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = latest_trans.id
                    uploaded.branch = latest_trans.branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_ype = "ElectricityPurchase"                          
                    uploaded.save()

                return HttpResponseRedirect(reverse('property:requisition_electricitypurchase', kwargs={'obj_id':latest_trans.id}))               
    return render(request, "property.html", context)

@login_required
@permission_required('office.edit_electricitymeternumber', raise_exception=True)
def editElectricityPurchase(request, obj_id): 
    title = "Edit Electricity Purchase"  
    transaction = ElectricityPurchase.objects.get(pk=obj_id) 
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    meter_number = ElectricityMeterNumber.objects.get(meter_number=transaction.meter_number)
    branch = Branch.objects.get(branch=meter_number.branch) 
    try:
        requisition = PFRequisition.objects.get(obj_id=obj_id,requisition_type="ElectricityPurchase")
    except PFRequisition.DoesNotExist:
        requisition = None   
    uploads = PFDocument.objects.filter(branch=branch).filter(obj_type="ElectricityPurchase").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = ElectricityPurchaseForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form":upload_file_form,
        "comment_form":comment_form,
        "uploads":uploads,
        "sliders":images,
        "comments":comments,
        
        }

    post = request.POST
    if request.POST:        
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save_form.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)                   
                    new_comment.branch = branch
                    new_comment.comment_type = "ElectricityPurchase"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.obj_id = transaction.id
                    uploaded.branch = branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_type = "ElectricityPurchase"
                    uploaded.save() 
               
                if request.user.has_perm('authorize_electricitypurchase'):
                    if requisition:   
                        return HttpResponseRedirect(reverse('property:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('property:propertyauthorizations'))
                else:
                    return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))     
    return render(request, "property.html", context)


@login_required
@permission_required('offices.view_electricitypurchase', raise_exception=True)
def electricityPurchaseList(request):
    title = "Electricity Purchases List"    
    purchase_list = ElectricityPurchase.objects.all().order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_purchase_list' in request.GET and filter_form.is_valid():
        purchase_list = filter_form.filter(purchase_list, date)   
    page = request.GET.get('page', 1)
    purchase_list_paginator = Paginator(purchase_list, 14)
    try:
        purchase_list = purchase_list_paginator.page(page)
    except PageNotAnInteger:
        purchase_list = purchase_list_paginator.page(1)
    except EmptyPage:
        purchase_list = purchase_list_paginator.page(purchase_list_paginator.num_pages)

    context ={
        "title": title,
        "purchase_list": purchase_list,        
        "filter_form": filter_form,       
        }       
    return render(request, "electricityPurchaseList.html", context)


@login_required
@permission_required('offices.create_mobilepurchase', raise_exception=True)
def mobilePurchase(request, obj_id):
    title = "Mobile Purchase"
    
    branch = Branch.objects.get(pk=obj_id)    
    purchase = MobilePurchase(branch = branch)

    form = MobilePurchaseForm(request.POST or None, instance=purchase, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(branch=branch, obj_type="MobilePurchase")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    

    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                latest_trans = MobilePurchase.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "MobilePurchase"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = latest_trans.id
                    uploaded.branch = latest_trans.branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_ype = "MobilePurchase"                          
                    uploaded.save()

                return HttpResponseRedirect(reverse('property:requisition_mobilepurchase', kwargs={'obj_id':latest_trans.id}))               
    return render(request, "property.html", context)

@login_required
@permission_required('offices.edit_mobilepurchase', raise_exception=True)
def editMobilePurchase(request, obj_id): 
    title = "Edit Mobile Purchase"  
    transaction = MobilePurchase.objects.get(pk=obj_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    branch = transaction.branch
    branch_id = Branch.objects.filter(branch=branch)
    branch = Branch.objects.get(pk=branch_id) 
    try:
        requisition = PFRequisition.objects.get(obj_id=obj_id, requisition_type="MobilePurchase")
    except PFRequisition.DoesNotExist:
        requisition = None   
    uploads = PFDocument.objects.filter(branch=branch).filter(obj_type="MobilePurchase").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = MobilePurchaseForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form":upload_file_form,
        "comment_form":comment_form,
        "uploads":uploads,
        "sliders":images,
        "comments":comments,
        
        }

    post = request.POST
    if request.POST:        
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)                   
                    new_comment.branch = branch
                    new_comment.comment_type = "MobilePurchase"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.obj_id = transaction.id
                    uploaded.branch = branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_type = "MobilePurchase"
                    uploaded.save() 
               
                if request.user.has_perm('authorize_mobilepurchase'):
                    if requisition:   
                        return HttpResponseRedirect(reverse('property:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('property:propertyauthorizations'))
                else:
                    return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))     
    return render(request, "property.html", context)


@login_required
@permission_required('offices.view_mobilepurchase', raise_exception=True)
def mobilePurchaseList(request):
    title = "Mobile Purchases List"    
    purchase_list = MobilePurchase.objects.all().order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_purchase_list' in request.GET and filter_form.is_valid():
        purchase_list = filter_form.filter(purchase_list, date)   
    page = request.GET.get('page', 1)
    purchase_list_paginator = Paginator(purchase_list, 14)
    try:
        purchase_list = purchase_list_paginator.page(page)
    except PageNotAnInteger:
        purchase_list = purchase_list_paginator.page(1)
    except EmptyPage:
        purchase_list = purchase_list_paginator.page(purchase_list_paginator.num_pages)

    context ={
        "title": title,
        "purchase_list": purchase_list,        
        "filter_form": filter_form,       
        }       
    return render(request, "mobilePurchaseList.html", context)


@login_required
@permission_required('propfac.create_propertymaintenance', raise_exception=True)
def propertyMaintenance(request, obj_id):
    title = "Property Maintenence"
    branch = Branch.objects.get(pk=obj_id)    
    inspection = PropertyMaintenance(branch = branch)

    form = PropertyMaintenanceForm(request.POST or None, instance=inspection, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(branch=branch, obj_type="PropertyMaintenance")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    

    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                latest_trans = PropertyMaintenance.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "PropertyMaintenance"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = latest_trans.id
                    uploaded.branch = latest_trans.branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_ype = "PropertyMaintenance"                          
                    uploaded.save()

                return HttpResponseRedirect(reverse('property:requisition_propertymaintenance', kwargs={'obj_id':latest_trans.id}))               
    return render(request, "property.html", context)


@login_required
@permission_required('propfac.edit_propertymaintenance', raise_exception=True)
def editPropertyMaintenance(request, obj_id): 
    title = "Edit branch Inspection"  
    transaction = PropertyMaintenance.objects.get(pk=obj_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    branch = transaction.branch
    branch_id = Branch.objects.filter(branch=branch)
    branch = Branch.objects.get(pk=branch_id) 
    try:
        requisition = PFRequisition.objects.get(obj_id=obj_id, requisition_type="PropertyMaintenance")
    except PFRequisition.DoesNotExist:
        requisition = None   
    uploads = PFDocument.objects.filter(branch=branch).filter(obj_type="PropertyMaintenance").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = PropertyMaintenanceForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form":upload_file_form,
        "comment_form":comment_form,
        "uploads":uploads,
        "sliders":images,
        "comments":comments,
        
        }

    post = request.POST
    if request.POST:        
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save_form.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)                   
                    new_comment.branch = branch
                    new_comment.comment_type = "PropertyMaintenance"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.obj_id = transaction.id
                    uploaded.branch = branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_type = "PropertyMaintenance"
                    uploaded.save() 
               
                if request.user.has_perm('authorize_propertymaintenance'):
                    if requisition:   
                        return HttpResponseRedirect(reverse('property:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('property:propertyauthorizations'))
                else:
                    return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))     
    return render(request, "property.html", context)


@login_required
@permission_required('propfac.view_propertymaintenance', raise_exception=True)
def propertyMaintenanceList(request):
    title = "Property Maintenance"    
    maintenance_list = PropertyMaintenance.objects.all().order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_maintenance_list' in request.GET and filter_form.is_valid():
        maintenance_list = filter_form.filter(maintenance_list, date)   
    page = request.GET.get('page', 1)
    maintenance_list_paginator = Paginator(maintenance_list, 14)
    try:
        maintenance_list = maintenance_list_paginator.page(page)
    except PageNotAnInteger:
        maintenance_list = maintenance_list_paginator.page(1)
    except EmptyPage:
        maintenance_list = maintenance_list_paginator.page(maintenance_list_paginator.num_pages)

    context ={
        "title": title,
        "maintenance_list": maintenance_list,        
        "filter_form": filter_form,       
        }       
    return render(request, "propertyMaintenanceList.html", context)


@login_required
@permission_required('propfac.create_officeinspection', raise_exception=True)
def officeInspection(request, obj_id):
    title = "Office Inspection"
    branch = Branch.objects.get(pk=obj_id)    
    inspection = OfficeInspection(branch = branch)
    form = OfficeInspectionForm(request.POST or None, instance=inspection, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(branch=branch, obj_type="OfficeInspection")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    

    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                latest_trans = OfficeInspection.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "OfficeInspection"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = latest_trans.id
                    uploaded.branch = latest_trans.branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_ype = "OfficeInspection"                          
                    uploaded.save()

                return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))               
    return render(request, "property.html", context)


@login_required
@permission_required('propfac.edit_officeinspection', raise_exception=True)
def editOfficeInspection(request, obj_id): 
    title = "Edit branch Inspection"  
    transaction = OfficeInspection.objects.get(pk=obj_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    branch = transaction.branch
    branch_id = Branch.objects.filter(branch=branch)
    branch = Branch.objects.get(pk=branch_id)    
    uploads = PFDocument.objects.filter(branch=branch).filter(obj_type="OfficeInspection").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = OfficeInspectionForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form":upload_file_form,
        "comment_form":comment_form,
        "uploads":uploads,
        "sliders":images,
        "comments":comments,
        
        }

    post = request.POST
    if request.POST:        
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save_form.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)                   
                    new_comment.branch = branch
                    new_comment.comment_type = "OfficeInspection"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.obj_id = transaction.id
                    uploaded.branch = branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_type = "OfficeInspection"
                    uploaded.save() 
               
                return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))        
    return render(request, "property.html", context)


@login_required
@permission_required('propfac.create_toiletinspection', raise_exception=True)
def officeToiletInspection(request, obj_id):
    title = "Office Toilet Inspection"
    
    branch = Branch.objects.get(pk=obj_id)    
    inspection = ToiletInspection(branch = branch)
    form = ToiletInspectionForm(request.POST or None, instance=inspection, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(branch=branch, obj_type="ToiletInspection")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    

    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                latest_trans = ToiletInspection.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "ToiletInspection"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = latest_trans.id
                    uploaded.branch = latest_trans.branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_ype = "ToiletInspection"                          
                    uploaded.save()

                return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))               
    return render(request, "property.html", context)


@login_required
@permission_required('propfac.edit_toiletinspection', raise_exception=True)
def editOfficeToiletInspection(request, obj_id): 
    title = "Edit branch Inspection"  
    transaction = ToiletInspection.objects.get(pk=obj_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    branch = transaction.branch
    branch_id = Branch.objects.filter(branch=branch)
    branch = Branch.objects.get(pk=branch_id)    
    uploads = PFDocument.objects.filter(branch=branch).filter(obj_type="ToiletInspection").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = ToiletInspectionForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form":upload_file_form,
        "comment_form":comment_form,
        "uploads":uploads,
        "sliders":images,
        "comments":comments,
        
        }

    post = request.POST
    if request.POST:        
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save_form.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)                   
                    new_comment.branch = branch
                    new_comment.comment_type = "ToiletInspection"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.obj_id = transaction.id
                    uploaded.branch = branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_type = "ToiletInspection"
                    uploaded.save() 
               
                return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))        
    return render(request, "property.html", context)


@login_required
@permission_required('propfac.view_officeinspection' or 'propfac.view_toiletinspection', raise_exception=True)
def inspectionsList(request):
    title = "Office Inspections"    
    inspections = OfficeInspection.objects.all().order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_inspections' in request.GET and filter_form.is_valid():
        inspections = filter_form.filter(inspections, date)   
    page = request.GET.get('page', 1)
    inspections_paginator = Paginator(inspections, 14)
    try:
        inspections = inspections_paginator.page(page)
    except PageNotAnInteger:
        inspections = inspections_paginator.page(1)
    except EmptyPage:
        inspections = inspections_paginator.page(inspections_paginator.num_pages)

    toilet_inspections = ToiletInspection.objects.all().order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_toilet_inspections' in request.GET and filter_form.is_valid():
        toilet_inspections = filter_form.filter(toilet_inspections, date)   
    page = request.GET.get('page', 1)
    toilet_inspections_paginator = Paginator(toilet_inspections, 14)
    try:
        toilet_inspections = toilet_inspections_paginator.page(page)
    except PageNotAnInteger:
        toilet_inspections = toilet_inspections_paginator.page(1)
    except EmptyPage:
        toilet_inspections = toilet_inspections_paginator.page(toilet_inspections_paginator.num_pages)

    context ={
        "title": title,
        "inspections": inspections,
        "toilet_inspections": toilet_inspections,
        "filter_form": filter_form,       
        }       
    return render(request, "officeInspectionsList.html", context)


@login_required
@permission_required('propfac.create_leaseagreementrenewal', raise_exception=True)
def renewLeaseAgreement(request, obj_id):
    title = "Renew Lease Agreement"
    
    lease = LeaseAgreement.objects.get(pk=obj_id)
    branch = Branch.objects.get(pk=lease.branch.id)    
    renewal = LeaseAgreementRenewal(branch=branch, expiry_date=lease.lease_expiry_date, rental_amount=lease.rental_amount)

    form = RenewLeaseForm(request.POST or None, instance=renewal, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(branch=branch, obj_type="LeaseAgreementRenewal")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
               
                lease.lease_expiry_date = renewal.new_expiry_date
                lease.rental_amount = renewal.rental_amount
                lease.save()

                latest_trans = LeaseAgreementRenewal.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "LeaseAgreementRenewal"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = latest_trans.id
                    uploaded.branch = latest_trans.branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_ype = "LeaseAgreementRenewal"                          
                    uploaded.save()

                return HttpResponseRedirect(reverse('property:requisition_leaseagreement_renewal', kwargs={'obj_id':latest_trans.id})) 
    return render(request, "property.html", context)


@login_required
@permission_required('propfac.edit_leaseagreementrenewal', raise_exception=True)
def editLeaseAgreementRenwal(request, obj_id): 
    title = "Edit Lease Agreement"  
    transaction = LeaseAgreementRenewal.objects.get(pk=obj_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    branch = transaction.branch
    branch_id = Branch.objects.filter(branch=branch)
    branch = Branch.objects.get(pk=branch_id)
    try:
        requisition = PFRequisition.objects.get(obj_id=obj_id, requisition_type="LeaseAgreementRenewal")
    except PFRequisition.DoesNotExist:
        requisition = None
    uploads = PFDocument.objects.filter(branch=branch).filter(obj_type="LeaseAgreementRenewal").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = RenewLeaseForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form":upload_file_form,
        "comment_form":comment_form,
        "uploads":uploads,
        "sliders":images,
        "comments":comments,
        
        }

    post = request.POST
    if request.POST:        
        if u'save' in post:
            valid_form = form.is_valid()            
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save_form.modified_by=request.user
                save_form.save()                

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = branch
                    new_comment.comment_type = "LeaseAgreementRenewal"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user

                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.obj_id = transaction.id
                    uploaded.branch = branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_type = "LeaseAgreementRenewal"
                    uploaded.save() 

                
                if request.user.has_perm('authorize_leaseagreement'):
                    if requisition:   
                        return HttpResponseRedirect(reverse('property:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('property:propertyauthorizations'))
                else:
                    return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id})) 
    return render(request, "property.html", context)

@login_required
@permission_required('propfac.create_leaseagreement', raise_exception=True)
def addLeaseAgreement(request, obj_id):
    title = "Add Lease Agreement"
    branch = Branch.objects.get(pk=obj_id)
    lease = LeaseAgreement()
    lease.branch = branch
    form = LeaseAgreementForm(request.POST or None, instance=lease, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(branch=branch, obj_type="LeaseAgreement")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)


    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                latest_trans = LeaseAgreement.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "LeaseAgreement"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = latest_trans.id
                    uploaded.branch = latest_trans.branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_ype = "LeaseAgreement"                          
                    uploaded.save()

                excess = form.cleaned_data.get('excess', None)
                return HttpResponseRedirect(reverse('property:requisition_leaseagreement', kwargs={'obj_id':latest_trans.id}))               
    return render(request, "property.html", context)


@login_required
@permission_required('propfac.edit_leaseagreement', raise_exception=True)
def editLeaseAgreement(request, obj_id): 
    title = "Edit Lease Agreement"  
    transaction = LeaseAgreement.objects.get(pk=obj_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    branch = transaction.branch
    branch_id = Branch.objects.filter(branch=branch)
    branch = Branch.objects.get(pk=branch_id)
    try:
        requisition = PFRequisition.objects.get(obj_id=obj_id, requisition_type="LeaseAgreement")
    except PFRequisition.DoesNotExist:
        requisition = None
    uploads = PFDocument.objects.filter(branch=branch).filter(obj_type="LeaseAgreement").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = LeaseAgreementForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context ={
        "title": title,
        "form": form,
        "branch": branch,
        "upload_file_form":upload_file_form,
        "comment_form":comment_form,
        "uploads":uploads,
        "sliders":images,
        "comments":comments,
        
        }

    post = request.POST
    if request.POST:        
        if u'save' in post:
            valid_form = form.is_valid()            
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save_form.modified_by=request.user
                save_form.save()
                
                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = branch
                    new_comment.comment_type = "LeaseAgreement"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.obj_id = transaction.id
                    uploaded.branch = branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_type = "LeaseAgreement"
                    uploaded.save() 

                
                if request.user.has_perm('authorize_leaseagreement'):
                    if requisition:   
                        return HttpResponseRedirect(reverse('property:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('property:propertyauthorizations'))
                else:
                    return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id})) 
    return render(request, "property.html", context)

@login_required
@permission_required('propfac.view_leaseagreement' or 'propfac.view_leaseagreementrenewal' , raise_exception=True)
def LeaseAgreementList(request):
    title = "Lease Agreements List"    
    leases = LeaseAgreement.objects.all().order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_leases' in request.GET and filter_form.is_valid():
        leases = filter_form.filter(leases, date)   
    page = request.GET.get('page', 1)
    leases_paginator = Paginator(leases, 14)
    try:
        leases = leases_paginator.page(page)
    except PageNotAnInteger:
        leases = leases_paginator.page(1)
    except EmptyPage:
        leases = leases_paginator.page(leases_paginator.num_pages)

    pending_closure = LeaseAgreement.objects.filter(status='Pending Closure').order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_pending_closure' in request.GET and filter_form.is_valid():
        pending_closure = filter_form.filter(pending_closure, date)   
    page = request.GET.get('page', 1)
    pending_closure_paginator = Paginator(pending_closure, 14)

    try:
        pending_closure = pending_closure_paginator.page(page)
    except PageNotAnInteger:
        pending_closure = pending_closure_paginator.page(1)
    except EmptyPage:
        pending_closure = pending_closure_paginator.page(pending_closure_paginator.num_pages)


    closed = LeaseAgreement.objects.filter(status='Closed').order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_closed' in request.GET and filter_form.is_valid():
        closed = filter_form.filter(closed, date)   
    page = request.GET.get('page', 1)
    closed_paginator = Paginator(closed, 14)
    try:
        closed = closed_paginator.page(page)
    except PageNotAnInteger:
        closed = closed_paginator.page(1)
    except EmptyPage:
        closed = closed_paginator.page(closed_paginator.num_pages)


    due_expiry_date = datetime.now() + timedelta(+30)
    expired_date = datetime.now() + timedelta(-1)
    todays_date = datetime.now()+ timedelta()


    expired = LeaseAgreement.objects.filter(lease_expiry_date__lte=expired_date,).order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_expired' in request.GET and filter_form.is_valid():
        expired = filter_form.filter(expired, date)   
    page = request.GET.get('page', 1)
    expired_paginator = Paginator(expired, 14)
    try:
        expired = expired_paginator.page(page)
    except PageNotAnInteger:
        expired = expired_paginator.page(1)
    except EmptyPage:
        expired = expired_paginator.page(expired_paginator.num_pages)


    expiring = LeaseAgreement.objects.filter(lease_expiry_date__range=[todays_date, due_expiry_date]).order_by('-id')
    date = 'lease_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_expiring' in request.GET and filter_form.is_valid():
        expiring = filter_form.filter(expiring, date)   
    page = request.GET.get('page', 1)
    expiring_paginator = Paginator(expiring, 14)
    try:
        expiring = expiring_paginator.page(page)
    except PageNotAnInteger:
        expiring = expiring_paginator.page(1)
    except EmptyPage:
        expiring = expiring_paginator.page(expiring_paginator.num_pages)


    renewal = LeaseAgreementRenewal.objects.all().order_by('-id')
    date = 'new_expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_renewals' in request.GET and filter_form.is_valid():
        renewal = filter_form.filter(renewal, date)   
    page = request.GET.get('page', 1)
    renewal_paginator = Paginator(renewal, 14)
    try:
        renewal = renewal_paginator.page(page)
    except PageNotAnInteger:
        renewal = renewal_paginator.page(1)
    except EmptyPage:
        renewal = renewal_paginator.page(renewal_paginator.num_pages)
 

    context ={
        "title": title,
        "leases": leases,
        "pending_closure": pending_closure,
        "closed": closed,
        "expired": expired,
        "expiring": expiring,
        "renewal": renewal,
        "filter_form": filter_form,       
        }       
    return render(request, "leaseAgreementsList.html", context)

@login_required
# @permission_required('fleet.edit_vehicle', 'fleet.view vehicle',raise_exception=True)
def viewproperty (request, obj_id):
    title = "Property Details"  
    filter_form = TransactionsFilterForm(request.POST or None)
    branch = None
    if filter_form.is_valid():       
        term = filter_form.cleaned_data.get('branch')
        branch = Branch.objects.all()
        if term:
            branch = branch.filter(branch=term)
            branch = Branch.objects.get(pk=branch)
        else:
            branch = Branch.objects.get(pk=obj_id)

    if branch is None:
        branch = Branch.objects.get(pk=obj_id)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')    
    uploads = PFDocument.objects.filter(branch=branch, obj_id=branch.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,        
        "branch": branch,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "sliders": images,
        'filter_form': filter_form,
        "comments": comments,      
        
        }
    post = request.POST
    if request.POST: 
        if u'save' in post:
            comment = comment_form.is_valid()
            if comment:
                new_comment = comment_form.save(commit=False)                   
                new_comment.branch = branch
                new_comment.comment_type = "General Comment"
                new_comment.obj_id = branch.id
                new_comment.created_by = request.user                   
                new_comment.save()

                return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id})) 
    return render(request, "property.html", context)

@login_required
@permission_required('propfac.create_pfrequisition', raise_exception=True)
def requisition(request, obj_id, obj_type=None): 
    title = "Process Requisition"   
    obj = obj_type.objects.get(pk=obj_id)

    Type = obj_type
    if "LeaseAgreement" in str(Type):
        o_type = "LeaseAgreement" 
    if "LeaseAgreementRenewal" in str(Type):
        o_type = "LeaseAgreementRenewal"   
    if "PropertyMaintenance" in str(Type):
        o_type = "PropertyMaintenance"
    if "MobilePurchase" in str(Type):
        o_type = "MobilePurchase"   
    if "TelcomPABXContract" in str(Type):
        o_type = "TelcomPABXContract"
    if "TelcomPABXContractRenewal" in str(Type):
        o_type = "TelcomPABXContractRenewal"
    if "ElectricityPurchase" in str(Type):
        o_type = "ElectricityPurchase"
        meter_number = ElectricityMeterNumber.objects.get(meter_number=obj.meter_number)
        branch = Branch.objects.get(branch=meter_number.branch) 
    else:
        branch = Branch.objects.get(branch=obj.branch) 

    req = PFRequisition(obj_id=obj.id, branch=branch, requisition_type=o_type)
   
    form = RequisitionForm(request.POST or None, instance=req)
    
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(branch=branch).filter(obj_type=o_type)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = PFComment.objects.filter(branch = branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "branch": branch, 
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
            
    }

    post = request.POST
    if request.POST:
        if u'save' in post:            
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.obj_id = obj.id
                save_form.save()

                latest_trans = PFRequisition.objects.order_by('-id')[0]
                
                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = obj.branch
                    new_comment.comment_type = o_type
                    new_comment.obj_id = obj.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = obj.id
                    uploaded.branch = obj.branch
                    uploaded.file_name = uploaded.file.name
                    uploaded.transaction = o_type
                    uploaded.save()
                return HttpResponseRedirect(reverse('property:view_requisition', kwargs={'obj_id':latest_trans.id}))
    return render(request, "property.html", context)


@login_required
@permission_required('propfac.create_pfrequisitionitem', raise_exception=True)
def requisition_item(request, obj_id): 
    title = "Process Requisition Items"
   
    obj = PFRequisition.objects.get(pk=obj_id)
    req = PFRequisitionItem()
    req.requisition_no = obj
    branch = Branch.objects.get(branch=obj.branch) 
    form = RequisitionItemForm(request.POST or None, instance=req)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(branch=obj.branch).filter(obj_type='Requisition')
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = PFDocument.objects.filter(branch=obj.branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    requisition_items = PFRequisitionItem.objects.filter(requisition_no=obj_id)

    comments = PFComment.objects.filter(branch = obj.branch)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "branch": branch, 
        "upload_file_form": upload_file_form,
        "comment_form": comment_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "requisition_items": requisition_items,
        "requisition": obj,
            
    }

    post = request.POST
    if request.POST:
        if u'save' in post:          
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.obj_id = obj.id
                save_form.created_by=request.user
                save_form.save() 
                return HttpResponseRedirect(reverse('property:requisition_item', kwargs={'obj_id':obj.id}))

        if u'addClose' in post:          
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.obj_id = obj.id
                save_form.save()

                return HttpResponseRedirect(reverse('property:view_requisition', kwargs={'obj_id':obj.id}))
    return render(request, "property.html", context)

@login_required
@permission_required('propfac.view_pfrequisition' or 'propfac.view_pfrequisitionitem', raise_exception=True)
def view_requisition(request, obj_id): 
    title = "Requistion"   
    try:
        obj = PFRequisition.objects.get(pk=obj_id)
        employee = Employee.objects.get(pk=obj.requested_by_id)    
        branch = Branch.objects.get(pk=obj.branch_id)
        region = Region.objects.get(pk=branch.region_id)
        subject = 'Requisition for %s branch. '%(obj.branch)
        body = '%s for %s branch.'%(obj.description, obj.branch)
    except PFRequisition.DoesNotExist:
        obj = None
        employee = None
        branch = None
        region = None
        subject = ''
        body = ''
    
    context ={
        'title': title,
        'requisition': obj,
        'branch': branch,
        'employee': employee,
        'region': region,
        'budgeted':obj.budgeted,
        'http_origin': "http://%s" % request.get_host(),  # settings.BASE_URL
    }

    if u'send' in request.POST:        
        send_pdf("requisition.html", context,  ['callien@emeraldlife.co.za', 'lewisk@emeraldlife.co.za'], body, subject, 'Requisition.pdf')        
        return HttpResponseRedirect(reverse('property:propertyauthorizations')) 

    if u'close' in request.POST:
        if request.user.has_perm('authorize_vehiclemaintenance'):   
            return HttpResponseRedirect(reverse('property:propertyauthorizations'))
        else:
            return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))  

    if u'download' in request.POST:
        return download_pdf("req.html", context, 'Requisition.pdf')
    
   
    return render(request, "view_requisition.html", context)

@login_required
def send_pdf(template_src, context_dict, to_email_address, email_body, email_subject, filename=None ):    
    
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result)

    email = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, to_email_address)
    email.attach(filename, result.getvalue(), 'application/pdf')
    email.send()    

    result.close()

@login_required
def download_pdf(template_src, context_dict, filename=None):    
    DEBUG = False
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="%s"' % filename
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()   
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result)

    response.write(result.getvalue())    
    result.close()

    if not pdf.err:        
        if DEBUG is True:          
            return http.HttpResponse(html)
        else:

            return response
    return http.HttpResponse('Error while creating the pdf! %s' % cgi.escae(html))

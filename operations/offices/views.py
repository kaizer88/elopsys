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
from propfac.models import *
from offices.models import *
from employees.models import *
from offices.models import *
from django.db.models import Count, Sum, Q
import collections
import json
from sms.sms_helper import *
from fleet.views import handler400,handler403, handler404, handler500


@login_required
@permission_required('offices.create_telcompabxcontractrenewal', raise_exception=True)
def mobileNumbers(request):
    title = "Add Mobile Number"
    form = MobileNumberForm(request.POST or None, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(obj_type="MobileNumber")
    mobile_numbers = MobileNumber.objects.all()
    page = request.GET.get('page', 1)
    mobile_numbers_paginator = Paginator(mobile_numbers, 15)
    try:
        mobile_numbers = mobile_numbers_paginator.page(page)
    except PageNotAnInteger:
        mobile_numbers = mobile_numbers_paginator.page(1)
    except EmptyPage:
        mobile_numbers = mobile_numbers_paginator.page(mobile_numbers_paginator.num_pages)  
     

    context ={
        "title": title,
        "form": form,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "mobile_numbers":mobile_numbers,
        "uploads": uploads,       
               
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                latest_trans = MobileNumber.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.comment_type = "MobileNumber"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = latest_trans.id
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_ype = "MobileNumber"                          
                    uploaded.save()

                return HttpResponseRedirect(reverse('offices:mobilenumbers'))       
    return render(request, "mobiles.html", context)



@login_required
@permission_required('offices.edit_telcompabxcontractrenewal', raise_exception=True)
def editMobileNumber(request, obj_id): 
    title = "Edit Mobile Number"  
    transaction = MobileNumber.objects.get(pk=obj_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)     
    uploads = PFDocument.objects.filter(obj_type="MobileNumber", obj_id=transaction.id)   
    form = MobileNumberForm(request.POST or None, instance=transaction, user=request.user)
    mobile_numbers = MobileNumber.objects.all()
    page = request.GET.get('page', 1)
    mobile_numbers_paginator = Paginator(mobile_numbers, 15)
    try:
        mobile_numbers = mobile_numbers_paginator.page(page)
    except PageNotAnInteger:
        mobile_numbers = mobile_numbers_paginator.page(1)
    except EmptyPage:
        mobile_numbers = mobile_numbers_paginator.page(mobile_numbers_paginator.num_pages)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    comments = PFComment.objects.filter(obj_id = obj_id)
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
        "upload_file_form":upload_file_form,
        "comment_form":comment_form,
        "uploads":uploads,
        "comments":comments,
        "mobile_numbers":mobile_numbers,
        
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
                    new_comment.comment_type = "MobileNumber"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.obj_id = transaction.id
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_type = "MobileNumber"
                    uploaded.save()
                return HttpResponseRedirect(reverse('offices:mobilenumbers'))     
    return render(request, "mobiles.html", context)


@login_required
@permission_required('offices.create_telcompabxcontract', raise_exception=True)
def cardAllocation(request):
    title = "Sim And Fuel Card Allocation"
    form = CardAllocationForm(request.POST or None, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = PFDocument.objects.filter(obj_type="CardAllocation")
    
    card_allocations = CardAllocation.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    card_allocations_paginator = Paginator(card_allocations, 15)
    try:
        card_allocations = card_allocations_paginator.page(page)
    except PageNotAnInteger:
        card_allocations = card_allocations_paginator.page(1)
    except EmptyPage:
        card_allocations = card_allocations_paginator.page(card_allocations_paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "upload_file_form": upload_file_form,
        "comment_form":comment_form,
        "uploads": uploads,
        "card_allocations": card_allocations,
               
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                latest_trans = CardAllocation.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.comment_type = "CardAllocation"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.transaction_id = latest_trans.id
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_ype = "CardAllocation"                          
                    uploaded.save()

                return HttpResponseRedirect(reverse('offices:cardallocations'))               
    return render(request, "mobiles.html", context)



@login_required
@permission_required('offices.edit_telcompabxcontractrenewal', raise_exception=True)
def editCardAlloction(request, obj_id): 
    title = "Edit Sim And Fuel Card Allocation"  
    transaction = CardAllocation.objects.get(pk=obj_id)    
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id) or None     
    uploads = PFDocument.objects.filter(obj_type="CardAllocation", obj_id=transaction.id)   
    form = CardAllocationForm(request.POST or None, instance=transaction, user=request.user)
    card_allocations = CardAllocation.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    card_allocations_paginator = Paginator(card_allocations, 15)
    try:
        card_allocations = card_allocations_paginator.page(page)
    except PageNotAnInteger:
        card_allocations = card_allocations_paginator.page(1)
    except EmptyPage:
        card_allocations = card_allocations_paginator.page(card_allocations_paginator.num_pages)

    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    comments = PFComment.objects.filter(obj_id = obj_id)
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
        "upload_file_form":upload_file_form,
        "comment_form":comment_form,
        "uploads":uploads,
        "comments":comments,
        "card_allocations":card_allocations,
        
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
                    new_comment.comment_type = "CardAllocation"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    uploaded = upload_file_form.save(commit=False)
                    uploaded.obj_id = transaction.id
                    uploaded.file_name = uploaded.file.name
                    uploaded.obj_type = "CardAllocation"
                    uploaded.save()
                if request.user.has_perm('authorize_telcompabxcontract'):
                	return HttpResponseRedirect(reverse('property:propertyauthorizations'))
                else:
                    return HttpResponseRedirect(reverse('offices:cardallocations'))     
    return render(request, "mobiles.html", context)
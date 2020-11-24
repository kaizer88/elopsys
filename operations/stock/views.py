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
from accounts.models import *
from django.db.models import Count, Sum, Q
import collections
import json
from sms.sms_helper import *
from fleet.views import handler400,handler403, handler404, handler500


@login_required
@permission_required('stock.create_stockitem', raise_exception=True)
def addStockItem(request):
    title = "Add Stock Item"
    branch=Branch.objects.get(branch="Head Office")
    stock_item = StockItem()
    items_list = StockItem.objects.all().order_by('-id')  
    if u'filter_claims' in request.GET and filter_form.is_valid():
        items_list = filter_form.filter(items_list, date)   
    page = request.GET.get('page', 1)
    items_list_paginator = Paginator(items_list, 14)
    try:
        items_list = items_list_paginator.page(page)
    except PageNotAnInteger:
        items_list = items_list_paginator.page(1)
    except EmptyPage:
        items_list = items_list_paginator.page(items_list_paginator.num_pages)
    form = StockItemForm(request.POST or None, instance=stock_item, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc') 

    context ={
        "title": title,
        "form": form,       
        "upload_file_form": upload_file_form,
        "comment_form":comment_form, 
        "items_list":items_list,       
        "addnew":True,
        'branch':branch,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                latest_trans = StockItem.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.comment_type = "StockItem"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_ype = "StockItem"                          
                        uploaded.save()
                return HttpResponseRedirect(reverse('inventory:stockitems_list'))               
    return render(request, "property.html", context)


@login_required
@permission_required('stock.edit_stockitem', raise_exception=True)
def editStockItem(request, obj_id): 
    title = "Edit Stock Item"
    branch=Branch.objects.get(branch="Head Office")  
    transaction = StockItem.objects.get(pk=obj_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    items_list = StockItem.objects.all().order_by('-id')  
    if u'filter_claims' in request.GET and filter_form.is_valid():
        items_list = filter_form.filter(items_list, date)   
    page = request.GET.get('page', 1)
    items_list_paginator = Paginator(items_list, 14)
    try:
        items_list = items_list_paginator.page(page)
    except PageNotAnInteger:
        items_list = items_list_paginator.page(1)
    except EmptyPage:
        items_list = items_list_paginator.page(items_list_paginator.num_pages)
    uploads = STDocument.objects.filter(obj_type="StockItem", obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = STDocument.objects.filter(obj_type="StockItem", obj_id=transaction.id).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = StockItemForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = STComment.objects.filter(comment_type="StockItem", obj_id=transaction.id)
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
        "sliders":images,
        "comments":comments,
        "addnew":True,
        "items_list":items_list,
        'branch':branch,
        
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
                    new_comment.comment_type = "StockItem"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.obj_id = transaction.id
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_type = "StockItem"
                        uploaded.save() 
                   
                return HttpResponseRedirect(reverse('inventory:stockitems_list'))        
    return render(request, "property.html", context)


@login_required
@permission_required('stock.view_stockitem' , raise_exception=True)
def stockItemsList(request):
    title = "Stock Items"    
    items_list = StockItem.objects.all().order_by('-id')  
    if u'filter_claims' in request.GET and filter_form.is_valid():
        items_list = filter_form.filter(items_list, date)   
    page = request.GET.get('page', 1)
    items_list_paginator = Paginator(items_list, 14)
    try:
        items_list = items_list_paginator.page(page)
    except PageNotAnInteger:
        items_list = items_list_paginator.page(1)
    except EmptyPage:
        items_list = items_list_paginator.page(items_list_paginator.num_pages)

   

    context ={
        "title": title,
        "items_list": items_list,      
        }       
    return render(request, "stockItemsList.html", context)


@login_required
@permission_required('stock.create_branchstock', raise_exception=True)
def branchStockItem(request, obj_id):
    title = "Branch Stock Items"
    
    branch = Branch.objects.get(pk=obj_id)    
    item = BranchStock(branch = branch)
    items_list = BranchStock.objects.filter(branch_id=obj_id)

    form = BranchStockForm(request.POST or None, instance=item, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = STDocument.objects.filter(branch=branch, obj_type="BranchStock")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = STDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]


    comments = STComment.objects.filter(branch = branch)
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
        "items_list": items_list,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                latest_trans = BranchStock.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "BranchStock"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.branch = latest_trans.branch
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_ype = "BranchStock"                          
                        uploaded.save()

                return HttpResponseRedirect(reverse('inventory:add_branchstockitem', kwargs={'obj_id':obj_id}))               
    return render(request, "property.html", context)


@login_required
@permission_required('stock.edit_branchstock', raise_exception=True)
def editBranchStockItem(request, obj_id): 
    title = "Branch Stock Items"  
    transaction = BranchStock.objects.get(pk=obj_id) 
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    branch = transaction.branch
    branch_id = Branch.objects.filter(branch=branch)
    branch = Branch.objects.get(pk=branch_id) 
    items_list = BranchStock.objects.filter(branch_id=branch_id)
    try:
        requisition = STRequisition.objects.get(obj_id=obj_id, requisition_type="BranchStock")
    except STRequisition.DoesNotExist:
        requisition = None   
    uploads = STDocument.objects.filter(branch=branch).filter(obj_type="BranchStock").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = STDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = BranchStockForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = STComment.objects.filter(branch = branch)
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
        "items_list":items_list,
        "edit_stock":True,
        
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
                    new_comment.comment_type = "BranchStock"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.obj_id = transaction.id
                        uploaded.branch = branch
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_type = "BranchStock"
                        uploaded.save()
                  
            	return HttpResponseRedirect(reverse('inventory:add_branchstockitem', kwargs={'obj_id':branch.id}))     
    return render(request, "property.html", context)



@login_required
@permission_required('stock.create_stockreplenishment', raise_exception=True)
def stockItemReplenishment(request, obj_id):
    title = "Branch Stock Items Replenishment"
    
    branch = Branch.objects.get(pk=obj_id) 
    stock_item = BranchStock.objects.first()
    item = StockReplenishment(branch = branch, item=stock_item.item)   
    items_list = BranchStock.objects.filter(branch_id=obj_id)

    form = StockReplenishmentForm(request.POST or None, instance=item, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = STDocument.objects.filter(branch=branch, obj_type="StockReplenishment")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = STDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]


    comments = STComment.objects.filter(branch = branch)
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
        "items_list": items_list,
        "replenish_stock":True,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                latest_trans = StockReplenishment.objects.order_by('-id')[0]
                stock_item.quantity += latest_trans.quantity
                stock_item.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "StockReplenishment"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.branch = latest_trans.branch
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_ype = "StockReplenishment"                          
                        uploaded.save()

                return HttpResponseRedirect(reverse('inventory:add_stockitemreplenishment', kwargs={'obj_id':obj_id }))               
    return render(request, "property.html", context)

@login_required
@permission_required('stock.create_stockreplenishment', raise_exception=True)
def stockItemsReplenishment(request, obj_id):
    title = "Branch Stock Items Replenishment"    
   
    stock_item = BranchStock.objects.get(pk=obj_id)
    branch = Branch.objects.get(id=stock_item.branch_id) 
    item = StockReplenishment(branch = branch, item=stock_item.item)   
    items_list = BranchStock.objects.filter(branch=branch)

    form = StockReplenishmentForm(request.POST or None, instance=item, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = STDocument.objects.filter(branch=branch, obj_type="StockReplenishment")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = STDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]


    comments = STComment.objects.filter(branch = branch)
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
        "items_list": items_list,
        "replenish_stock":True,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                latest_trans = StockReplenishment.objects.order_by('-id')[0]
                stock_item.quantity += latest_trans.quantity
                stock_item.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "StockReplenishment"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.branch = latest_trans.branch
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_ype = "StockReplenishment"                          
                        uploaded.save()

                return HttpResponseRedirect(reverse('inventory:add_stockitemreplenishment', kwargs={'obj_id':branch.id }))               
    return render(request, "property.html", context)


@login_required
@permission_required('stock.edit_stockreplenishment', raise_exception=True)
def editStockItemReplenishment(request, obj_id): 
    title = "Stock Items Replenishment"  
    transaction = StockReplenishment.objects.get(pk=obj_id) 
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    branch = transaction.branch
    branch_id = Branch.objects.filter(branch=branch)
    branch = Branch.objects.get(pk=branch_id) 
    items_list = StockReplenishment.objects.filter(branch_id=branch_id, id=obj_id)
    try:
        requisition = STRequisition.objects.get(obj_id=obj_id, requisition_type="StockReplenishment")
    except STRequisition.DoesNotExist:
        requisition = None   
    uploads = STDocument.objects.filter(branch=branch).filter(obj_type="StockReplenishment").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = STDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = StockReplenishmentForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = STComment.objects.filter(branch = branch)
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
        "items_list":items_list,
        
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
                    new_comment.comment_type = "StockReplenishment"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.obj_id = transaction.id
                        uploaded.branch = branch
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_type = "StockReplenishment"
                        uploaded.save()
                  
            	return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))     
    return render(request, "property.html", context)


@login_required
@permission_required('stock.view_stockreplenishment' , raise_exception=True)
def stockReplenishmentList(request):
    title = "Stock Items Replenishment"    
    items_list = StockReplenishment.objects.all().order_by('-id')  
    if u'filter_claims' in request.GET and filter_form.is_valid():
        items_list = filter_form.filter(items_list, date)   
    page = request.GET.get('page', 1)
    items_list_paginator = Paginator(items_list, 14)
    try:
        items_list = items_list_paginator.page(page)
    except PageNotAnInteger:
        items_list = items_list_paginator.page(1)
    except EmptyPage:
        items_list = items_list_paginator.page(items_list_paginator.num_pages)


    context ={
        "title": title,
        "items_list": items_list,      
        }       
    return render(request, "stockReplenishmentList.html", context)

@login_required
@permission_required('stock.create_stockreplenishment', raise_exception=True)
def applicationBooks(request):
    title = "Application Book Replenishment"   
   
    application_book = Book.objects.first()
    books = Book.objects.all()
    item = BookReplenishment(book = application_book, in_stock=application_book.quantity)
    branch = Branch.objects.get(branch="Head Office") 

    form = BookReplenishmentForm(request.POST or None, instance=item, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = STDocument.objects.filter(branch=branch, obj_type="BookReplenishment")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = STDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]


    comments = STComment.objects.filter(branch = branch)
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
        "books": books,
        "replenish_stock":True,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                latest_trans = StockReplenishment.objects.order_by('-id')[0]
                stock_item.quantity += latest_trans.quantity
                stock_item.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "BookReplenishment"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.branch = latest_trans.branch
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_ype = "BookReplenishment"                          
                        uploaded.save()

                return HttpResponseRedirect(reverse('inventory:add_stockitemreplenishment', kwargs={'obj_id':obj_id, 'trans_id':trans_id}))               
    return render(request, "property.html", context)


@login_required
@permission_required('stock.create_stockreplenishment', raise_exception=True)
def bookReplenishment(request, obj_id):
    title = "Application Book Replenishment"   
   
    application_book = Book.objects.get(pk=obj_id)
    books = Book.objects.all()
    item = BookReplenishment(book = application_book, in_stock=application_book.quantity)
    branch = Branch.objects.get(branch="Head Office") 

    form = BookReplenishmentForm(request.POST or None, instance=item, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = STDocument.objects.filter(branch=branch, obj_type="BookReplenishment")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = STDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]


    comments = STComment.objects.filter(branch = branch)
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
        "books": books,
        "replenish_stock":True,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                latest_trans = StockReplenishment.objects.order_by('-id')[0]
                stock_item.quantity += latest_trans.quantity
                stock_item.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "BookReplenishment"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.branch = latest_trans.branch
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_ype = "BookReplenishment"                          
                        uploaded.save()

                return HttpResponseRedirect(reverse('inventory:add_stockitemreplenishment', kwargs={'obj_id':obj_id, 'trans_id':trans_id}))               
    return render(request, "property.html", context)



@login_required
@permission_required('stock.create_stocktake', raise_exception=True)
def stockTake(request, obj_id):
    title = "Stock Take"
    
    branch = Branch.objects.get(pk=obj_id) 
    stock_item = BranchStock.objects.first() 
    item = StockTake(branch = branch, item=stock_item.item)   
    items_list = BranchStock.objects.filter(branch_id=obj_id)

    form = StockTakeForm(request.POST or None, instance=item, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = STDocument.objects.filter(branch=branch, obj_type="StockTake")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = STDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]


    comments = STComment.objects.filter(branch = branch)
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
        "items_list": items_list,
        "stock_take":True,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                latest_trans = StockTake.objects.order_by('-id')[0]

                floors = Floor.objects.filter(branch=branch)
                stock_count = 0
                for floor in floors:
                	floor_stock = StockTake.objects.filter(floor=floor,item=latest_trans.item).order_by('-id')[0]
                	stock_count += floor_stock.quantity
                stock_item.quantity = stock_count
                stock_item.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "StockTake"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.branch = latest_trans.branch
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_ype = "StockTake"                          
                        uploaded.save()

                return HttpResponseRedirect(reverse('inventory:add_stocktake', kwargs={'obj_id':obj_id, 'trans_id':trans_id}))               
    return render(request, "property.html", context)


@login_required
@permission_required('stock.create_stocktake', raise_exception=True)
def stockTaking(request, obj_id):
    title = "Stock Take"
    
    stock_item = BranchStock.objects.get(pk=obj_id)
    branch = Branch.objects.get(id=stock_item.branch_id)  
    item = StockTake(branch = branch, item=stock_item.item)   
    items_list = BranchStock.objects.filter(branch=branch)

    form = StockTakeForm(request.POST or None, instance=item, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = STDocument.objects.filter(branch=branch, obj_type="StockTake")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = STDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]


    comments = STComment.objects.filter(branch = branch)
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
        "items_list": items_list,
        "stock_take":True,
        
        }
                
    post = request.POST
    if request.POST:        
        if u'save' in post:         
            valid_form = form.is_valid()            
            if valid_form:              
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                latest_trans = StockTake.objects.order_by('-id')[0]

                floors = Floor.objects.filter(branch=branch)
                stock_count = 0
                for floor in floors:
                    floor_stock = StockTake.objects.filter(floor=floor,item=latest_trans.item).order_by('-id')[0]
                    stock_count += floor_stock.quantity
                stock_item.quantity = stock_count
                stock_item.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.branch = latest_trans.branch
                    new_comment.comment_type = "StockTake"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.branch = latest_trans.branch
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_ype = "StockTake"                          
                        uploaded.save()

                return HttpResponseRedirect(reverse('inventory:add_stocktake', kwargs={'obj_id':branch.id}))               
    return render(request, "property.html", context)


@login_required
@permission_required('stock.edit_stocktake', raise_exception=True)
def editStockTake(request, obj_id): 
    title = "Stock Items Replenishment"  
    transaction = StockTake.objects.get(pk=obj_id) 
    stock_item = BranchStock.objects.get(item=transaction.item) 
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    branch = transaction.branch
    branch_id = Branch.objects.filter(branch=branch)
    branch = Branch.objects.get(pk=branch_id) 
    items_list = StockTake.objects.filter(branch_id=branch_id, id=obj_id)
    try:
        requisition = STRequisition.objects.get(obj_id=obj_id, requisition_type="StockTake")
    except STRequisition.DoesNotExist:
        requisition = None   
    uploads = STDocument.objects.filter(branch=branch).filter(obj_type="StockTake").filter(obj_id=transaction.id)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = STDocument.objects.filter(branch=branch).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = StockTakeForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = STComment.objects.filter(branch = branch)
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
        "items_list":items_list,
        
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

                floors = Floor.objects.filter(branch=branch)
                stock_count = 0
                for floor in floors:
                	floor_stock = StockTake.objects.filter(floor=floor,item=transaction.item).order_by('-id')[0]
                	stock_count += floor_stock.quantity
                stock_item.quantity = stock_count
                stock_item.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)                   
                    new_comment.branch = branch
                    new_comment.comment_type = "StockTake"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user                   
                    new_comment.save()

                validated = upload_file_form.is_valid()             
                if validated:                   
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = STDocument.objects.create(file=f)
                        uploaded.obj_id = transaction.id
                        uploaded.branch = branch
                        uploaded.file_name = uploaded.file.name
                        uploaded.obj_type = "StockTake"
                        uploaded.save()
                  
            	return HttpResponseRedirect(reverse('property:viewproperty', kwargs={'obj_id':branch.id}))     
    return render(request, "property.html", context)


@login_required
@permission_required('stock.view_stocktake', raise_exception=True)
def stockTakeList(request):
    title = "Stock Take List"    
    items_list = StockTake.objects.all().order_by('-id')  
    if u'filter_claims' in request.GET and filter_form.is_valid():
        items_list = filter_form.filter(items_list, date)   
    page = request.GET.get('page', 1)
    items_list_paginator = Paginator(items_list, 14)
    try:
        items_list = items_list_paginator.page(page)
    except PageNotAnInteger:
        items_list = items_list_paginator.page(1)
    except EmptyPage:
        items_list = items_list_paginator.page(items_list_paginator.num_pages)


    context ={
        "title": title,
        "items_list": items_list,      
        }       
    return render(request, "stockTakeList.html", context)


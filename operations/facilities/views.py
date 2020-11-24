import os

from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Count, Sum, Q
from django.db.models.functions import Concat
from django.db.models import Value as V
import json
from employees.models import *
from facilities.models import *
from fleet_management.exporter import *
from fleet_management.importer import *
import threading
import re

from forms import StockItemForm, StockTransactionForm, StockItemImportForm
from forms import StockFilterForm, StockTransactionFilterForm

@login_required
@csrf_exempt
def get_opening_balance(request, item_id):
    stock_item = StockItem.objects.get(id=item_id)
   
    item = {}
    item['id'] = stock_item.id
    item['label'] = stock_item.item_name
    item['value'] = stock_item.stock_quantity or 0

    results = json.dumps(item)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
def stock_items_uploads(request, template="facilities/stock_uploads.html"):
    context = {}

    form = StockItemImportForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        import_stock_items_data(request.user, form.cleaned_data.get('stock_item_file'))

    context['form'] = form

    return render(request, template, context)

@login_required
def stock_items(request, template="facilities/stock_items.html"):
    context = {}
       
    stock_items = StockItem.objects.all() 
    stock_filter_form = StockFilterForm(request.GET or None)
    heading = "Stock Items"
    
    if u'filter' in request.GET or u'extract' in request.GET:
        if stock_filter_form.is_valid():
            stock_items = stock_filter_form.filter(stock_items)            

    if u'extract' in request.GET:
        download_thread = threading.Thread(target=extract_stock_items_data, 
                                           args=(request.user, 'all_stock_items', stock_items, 
                                                 stock_filter_form.cleaned_data))
        download_thread.start()
        messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

    context['stock_items'] = stock_items
    context['stock_filter_form'] = stock_filter_form
    context['heading'] = heading
    return render(request, template, context)


@login_required
def stock_items_transactions(request, template="facilities/stock_items_transactions.html"):
    context = {}
       
    stock_items = StockTransaction.objects.all() 
    stock_filter_form = StockTransactionFilterForm(request.GET or None)
    heading = "Stock Items Transactions"
    
    if u'filter' in request.GET or u'extract' in request.GET:
        if stock_filter_form.is_valid():
            stock_items = stock_filter_form.filter(stock_items)

    if u'extract' in request.GET:
        download_thread = threading.Thread(target=extract_stock_items_received_data, 
                                           args=(request.user, 'all_stock_items', stock_items, 
                                                 stock_filter_form.cleaned_data))
        download_thread.start()
        messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')
            
    context['stock_items'] = stock_items
    context['stock_filter_form'] = stock_filter_form
    context['heading'] = heading
    return render(request, template, context)

@login_required
def edit_stock_item(request, item_id=None, template="facilities/stock_item_edit.html", context=None):

    context = context or {}

    stock_item = StockItem.objects.get(pk=item_id) if item_id else None
    
    stock_item_form = StockItemForm(request.POST or None, instance=stock_item)

    if u'save' in request.POST:
        if stock_item_form.is_valid():
            stock_item = stock_item_form.save(request.user)
            stock_item.save()
            
            next = request.POST.get('next', '/')
            
            return HttpResponseRedirect(next)

    if u'cancel' in request.POST:
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    context['stock_item'] = stock_item
    context['stock_item_form'] = stock_item_form
    
    return render(request, template, context)


@login_required
def edit_stock_item_transaction(request, item_id=None, template="facilities/stock_item_transaction_edit.html", context=None):

    context = context or {}
    quantity = 0
    has_intsance = False
    opening_balance = 0
    stock_item = StockTransaction.objects.get(pk=item_id) if item_id else None
    if stock_item:
        quantity = stock_item.quantity
        opening_balance = stock_item.opening_stock
        transaction = stock_item.transaction_type
        stk = stock_item.stock_item
        has_intsance = True
       
    stock_item_form = StockTransactionForm(request.POST or None, instance=stock_item)
        
    if u'save' in request.POST:
        if stock_item_form.is_valid():
            stock_item = stock_item_form.save(commit=False)
            stock_item.modified_by = request.user
            stock_item.created_by = request.user
            if has_intsance:
                stock_item.opening_stock = opening_balance
                stock_item.stock_item = stk
                stock_item.transaction_type = transaction
            else:
                stock_item.opening_stock = stock_item.stock_item.stock_quantity or 0
            stock_item.save() 

            stock = stock_item.stock_item
            if not has_intsance:
                stock.stock_quantity = stock_item.stock_balance
                stock.modified_by_id = request.user
            else:
                if transaction == 'allocated':
                    stock.stock_quantity -= stock_item.quantity - quantity
                    stock.modified_by_id = request.user
                else:
                    stock.stock_quantity += stock_item.quantity - quantity
                    stock.modified_by_id = request.user
            stock.save()
            
            next = request.POST.get('next', '/')
            if 'edit' in next or 'add' in next:
                return redirect(reverse('facilities:stock_items_transactions'))
            return HttpResponseRedirect(next)
        

    if u'cancel' in request.POST:
        next = request.POST.get('next', '/')
        if 'edit' in next or 'add' in next:
            return redirect(reverse('facilities:stock_items_transactions'))
        return HttpResponseRedirect(next)

    context['stock_item'] = stock_item
    context['stock_item_form'] = stock_item_form
    
    return render(request, template, context)

@login_required
def stock_item_delete(request, item_id):

    stock_item = StockItem.objects.get(pk=item_id)
    stock_item.deleted = True
    stock_item.save()

    return redirect(reverse('facilities:stock_items'))
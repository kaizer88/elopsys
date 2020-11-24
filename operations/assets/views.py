# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.shortcuts import render

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

from models import Asset, AssetDetail, AssetPurchaseDetail

from forms import AssetForm, AssetFilterForm, AssetDetailForm, AssetPurchaseDetailForm

from operations.forms import AddressForm, ContactForm

from operations.models import *

from fleet_management.exporter import extract_asset_data

# Create your views here.

@login_required
@csrf_exempt
def get_districts(request, region_id):
    if region_id:
        districts = Branch.objects.filter(region__id=region_id)
    else:
        districts = Branch.objects.all()

    data = []

    for d in districts:
        district = {}
        district['id'] = d.id
        district['label'] = d.code +' - '+ d.description
        district['value'] = d.code +' - '+ d.description
        data.append(district)

    results = json.dumps(data)
    mimetype = 'application/json'

@login_required
def assets(request, template="assets/view_assets.html", context=None):
    context = context or {}

    assets = Asset.objects.all()

    filter_form = AssetFilterForm(request.GET or None)

    if u'search' in request.GET or u'extract' in request.GET:

        if filter_form.is_valid():
            assets = filter_form.filter(assets)

    if u'extract' in request.GET:
        download_thread = threading.Thread(target=extract_asset_data,
                                           args=(request.user, "assets",assets,
                                                 filter_form.cleaned_data))

        download_thread.start()
        messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

    context['assets'] = assets
    context['filter_form'] = filter_form

    return render(request, template, context)

@login_required
def edit_asset(request,  asset_id=None, template="assets/edit_asset.html", context=None):

    context = context or {}
    asset = None
    asset_detail = None
    asset_purchase_detail = None
    contact_person = None
    address = None

    if asset_id:
        asset = Asset.objects.get(pk=asset_id)

        asset_form = AssetForm(request.POST or None, instance=asset)

        if asset.asset_detail:
            asset_detail = AssetDetail.objects.get(pk=asset.asset_detail_id)
        asset_detail_form = AssetDetailForm(request.POST or None, instance=asset_detail)

        if asset.asset_purchase_detail:
            asset_purchase_detail = AssetPurchaseDetail.objects.get(pk=asset.asset_purchase_detail_id)
        asset_purchase_detail_form = AssetPurchaseDetailForm(request.POST or None, instance=asset_purchase_detail)

        if asset.contact_person:
            contact_person = Contact.objects.get(pk=asset.contact_person_id)
        contact_form = ContactForm(request.POST or None, instance=contact_person)
        if asset.address:
            address = Address.objects.get(pk=asset.address_id)
        address_form = AddressForm(request.POST or None, instance=address)
    else:
        asset_form = AssetForm(request.POST or None)
        asset_detail_form = AssetDetailForm(request.POST or None)
        asset_purchase_detail_form = AssetPurchaseDetailForm(request.POST or None)
        contact_form = ContactForm(request.POST or None)
        address_form = AddressForm(request.POST or None)

    if asset_detail_form.is_valid():
        asset_detail = asset_detail_form.save(commit=False)
        asset_detail.created_by = request.user
        asset_detail.save()

    if asset_purchase_detail_form.is_valid():
        asset_purchase_detail = asset_purchase_detail_form.save(commit=False)
        asset_purchase_detail.created_by = request.user
        asset_purchase_detail.save()

    if contact_form.is_valid():
        contact_person = contact_form.save(commit=False)
        contact_person.save()

    if address_form.is_valid():
        address = address_form.save(commit=False)
        address.address_type = 'business'
        address.save()

    if asset_form.is_valid():
        asset = asset_form.save(commit=False)
        asset.asset_detail = asset_detail
        asset.asset_purchase_detail = asset_purchase_detail
        asset.contact_person = contact_person
        asset.address = address
        asset.created_by = request.user
        if asset.category_one == 'stationery':
            asset.serial_number = None
        else:
            asset.asset_detail.quantity = None

        asset.save()

        return redirect(reverse('assets:view_assets'))

    context['asset_form'] = asset_form
    context['asset_detail_form'] = asset_detail_form
    context['purchase_detail_form'] = asset_purchase_detail_form
    context['asset'] = asset
    context['contact_form'] = contact_form
    context['address_form'] = address_form

    return render(request, template, context)


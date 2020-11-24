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
    url(r'^stock_items/$', views.stock_items, name='stock_items'),
    url(r'^stock_items/edit/(?P<item_id>\d+)/$', views.edit_stock_item, name='edit_stock_item'),
    url(r'^stock_items/add/$', views.edit_stock_item, name='add_stock_item'),    
    
    url(r'^get_opening_balance/(?P<item_id>\d+)/$', views.get_opening_balance, name='get_opening_balance'),

    url(r'^stock_items/uploads/$', views.stock_items_uploads, name='stock_items_uploads'),

    url(r'^stock_items/transactions/$', views.stock_items_transactions, name='stock_items_transactions'),
    url(r'^stock_items/transactions/edit/(?P<item_id>\d+)/$', views.edit_stock_item_transaction, name='edit_stock_item_transaction'),
    url(r'^stock_items/transactions/add/$', views.edit_stock_item_transaction, name='add_stock_item_transaction'),

    url(r'^stock_item_delete/(?P<item_id>\d+)/$', views.stock_item_delete, name='stock_item_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



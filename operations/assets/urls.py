from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
import views

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
from assets.models import *

urlpatterns = [
    url(r'^assets$', views.assets, name='view_assets'),
    url(r'^assets/edit/(?P<asset_id>\d+)/$', views.edit_asset, name='edit_asset'),
    url(r'^assets/add/$', views.edit_asset, name='add_asset'),
    url(r'^get_districts/(?P<region_id>\d+)/$', views.get_districts, name='get_districts'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
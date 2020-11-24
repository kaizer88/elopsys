from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django_js_reverse.views import urls_js
from models import RegionAutoComplete,DistrictAutoComplete

urlpatterns = [
    url(r'^region_autocomplete/$', RegionAutoComplete.as_view(), name='region_autocomplete'),
    url(r'^district_autocomplete/$', DistrictAutoComplete.as_view(), name='district_autocomplete'),    
    url(r'^$', views.home, name='home'),
    url(r'^jsreverse/$', urls_js, name='js_reverse'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout,{'next_page':'/'}, name='logout'),

    url(r'^about/$', views.about, name='about'),
    url(r'^users$', views.users, name='users'),
    url(r'^users/fleet-admins/(?P<fleet_administrators>\d+)/$', views.users, name='fleet_admins'),
    url(r'^user/add/$', views.user_edit, name='user_add'),
    url(r'^user/edit/(?P<user_id>\d+)/$', views.user_edit, name='user_edit'),
    
    
    url(r'^', include('fleet_management.urls', namespace='fleetmanagement')),
    url(r'^', include('employees.urls', namespace='employees')), 
    url(r'^', include('facilities.urls', namespace='facilities')),   
    url(r'^', include('assets.urls', namespace='assets')),
    url(r'^', include('api.urls', namespace='api')),

    url(r'^regions$', views.view_regions, name='view_regions'),
    url(r'^branches$', views.view_branches, name='view_branches'),

    url(r'^downloads/$', views.downloads_list, name="view_downloads"),
    url(r'^downloads/(?P<file_id>\d+)/$', views.file_download_task, name="file_download"),

    url(r'^tickets$', views.view_tickets, name='view_tickets'),
    url(r'^tickets/add$', views.edit_ticket, name='add_ticket'),
    url(r'^tickets/edit(?P<ticket_id>\d+)/$', views.edit_ticket, name='edit_ticket'),

    url(r'^service_provider/uploads$', views.service_provider_uploads, name='service_provider_uploads'),
    url(r'^districts/uploads$', views.district_uploads, name='district_uploads'),

    url(r'^accounts/user_profile/(?P<user_id>\-{0,1}\d+$)', views.user_profile, name='user_profile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

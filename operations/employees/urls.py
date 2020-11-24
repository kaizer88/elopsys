from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
import views

urlpatterns = [
    url(r'^employees/$', views.employees, name='employees'),
    url(r'^employees/edit/(?P<employee_id>\d+)/$', views.edit_employee, name='edit_employee'),
    url(r'^reports/drivers_licence_expiry$', views.drivers_licence_expiry, name='drivers_licence_expiry'),

]

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^dashboard/$', views.dash, name='dash'),
]

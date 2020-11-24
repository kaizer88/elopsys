from django.conf.urls import url, handler400, handler403, handler404, handler500
from . import views

handler400 = 'fleet.views.handler400'
handler403 = 'fleet.views.handler403'
handler404 = 'fleet.views.handler404'
handler500 = 'fleet.views.handler500'

urlpatterns = [

	url(r'^imports/$', views.imports, name='imports'),
	]
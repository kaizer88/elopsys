from django.conf.urls import include, url
from django.conf import settings
import views


urlpatterns = [
    url(r'^/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_vehicle_info/', views.get_vehicle_info),
    url(r'^push_agent_data/', views.push_agent_data),
    url(r'^push_region_data/', views.push_region_data),
    url(r'^push_branch_data/', views.push_branch_data),
]

from django.conf.urls import url

from . import views
urlpatterns = [
	url(r'^$', views.login_veiw, name='login'),
	url(r'^logout/$', views.logout_veiw, name='logout'),
	url(r'^accounts/registration/$', views.register_veiw, name='register'),
	url(r'^accounts/edit/user/(?P<user_id>\-{0,1}\d+$)', views.edit_user, name='editUser'),
	url(r'^accounts/users/$', views.users_list, name='usersList'),




]
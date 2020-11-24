from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
User = get_user_model()
from .forms import UserLoginForm, UserRegisterForm, fileUploadForm

# Create your views here.


def login_veiw(request):
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if  request.POST.get('auth_btn', None) and form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('home')

	return render(request, "login.html", {"form":form, "title":title})


def register_veiw(request):
	title = "Register User"
	form = UserRegisterForm(request.POST or None,  request.FILES or None)	
	if form.is_valid():
		user = form.save()
		password = form.cleaned_data.get('password')
		new_user = authenticate(username=user.username, password=password)

		return redirect('usersList')

	
	context = {
		"title": title,
		"form": form,		
	}
	return render(request, "register_user.html", context)

def edit_user(request, user_id):
	title = "Edit User"
	user = User.objects.get(pk=user_id)
	form =  UserRegisterForm(request.POST or None, request.FILES or None, instance=user,)
	if form.is_valid():
		user = form.save()
		return redirect('usersList')

	context = {
		"title": title,
		"form": form,		
	}
	return render(request, "register_user.html", context)	

def users_list(request):
	title = "Users List"
	users = User.objects.all()
	context={
		'users':users,
		'title':title,
	}
	return render(request, "users_list.html", context)


def logout_veiw( request):
	logout(request)
	return redirect('login')
	return render(request, "login.html", {})




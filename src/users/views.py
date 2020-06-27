from django.shortcuts import render,redirect

from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import logout
# Create your views here.

def login_view(request,*args,**kwargs):

	
	return render(request,"users/login.html",{})

def logout_view(request,*args,**kwargs):

	logout(request)
	return redirect('/login')

def register_view(request,*args,**kwargs):

	if request.method=='POST':
			form = UserRegisterForm(request.POST)
			if form.is_valid():
				form.save()
				# username=form.cleaned_data.get('username');
				# messages.success(request,f'Account created for {username}.')
				return redirect('home')
	else:
		form=UserRegisterForm()
	return render(request,"users/register.html",{'form':form})
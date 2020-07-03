from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from .forms import UserRegisterForm
from materials.forms import ProjectRegisterForm
# from materials.models import Proj
from chart.models import Schedule
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


# Create your views here.
# def register_project_view(request,*args,**kwargs):

# 	if request.method=='POST':
# 			form = ProjectRegisterForm(request.POST)
# 			if form.is_valid():
# 				form.save()
				
# 				return redirect('RequirementList')
# 	else:
# 		form=ProjectRegisterForm()
# 	return form

@login_required()
def home_view(request,*args,**kwargs):
	# class table_view(ListView):
	# template_name="materials/listview.html"
	# queryset = Requirement.objects.all()
	schedule_list = Schedule.objects.filter(added_by=request.user)
	if not schedule_list:
		first_project = Schedule(name="Sample Project",is_selected=True,added_by=request.user,progress_schedule=0)
		first_project.save()
		print('saved')


	else:
		
		project_id = request.GET.get('project')
		first_project= schedule_list.first()
		first_project.is_selected=True
		first_project.save()
	
	project_selected = Schedule.objects.filter(added_by=request.user,is_selected=True)
	
	
	if request.method == 'GET' and 'project' in request.GET:
		q = request.GET['project']
		if q is not None and q != '':	
			project_selected = Schedule.objects.filter(added_by=request.user,id=project_id)
			for project in schedule_list:
				project.is_selected=False
				project.save()
			
				
			for project in project_selected:
				first_project.is_selected=False
				first_project.save()
				project.is_selected=True
				project.save()
	# object_list = Proj.objects.all()
			
	if request.method=='POST':
			form = ProjectRegisterForm(request.POST)
    
        	
			if form.is_valid():
				obj = form.save()
				obj.added_by = request.user
				obj.save()
				# return redirect('pagedetail', page_id=obj.id)
				return redirect('home')
	else:
		form=ProjectRegisterForm()

	if request.method=='POST':
			form1 = UserRegisterForm(request.POST)
			if form1.is_valid():
				save_it = form1.save()
				save_it.save()
				# subject="Thanks for registering with us"
				# message = "welcome "
				# from_email = settings.EMAIL_HOST_USER
				# to_list = [save_it.email , settings.EMAIL_HOST_USER]
				# send_mail(subject,message,from_email,to_list)
				# to turn off errors add fail_silently = True as an arguement to send_mail
				username=form1.cleaned_data.get('username');
				messages.success(request,f'Account created for {username}.')
				return redirect('home')
	else:
		form1=UserRegisterForm()
	selected_project= project_selected.first()

	context = {
	# 'object_list' : object_list,
	'form' : form,
	'form1' : form1,
	'schedule_list' : schedule_list,
	'project_selected' : project_selected,
	'project_list_first': selected_project

	}
	return render(request,"projects/home.html",context)

@login_required()
def en_upload_SG_view(request,*args,**kwargs):
	return render(request,"projects/en-upload-SG.html",{})
@login_required()
def register_view(request,*args,**kwargs):
	if request.method=='POST':
			form = UserRegisterForm(request.POST)
			if form.is_valid():
				save_it = form.save()
				save_it.save()
				subject="Thanks for registering with us"
				message = "welcome "
				from_email = settings.EMAIL_HOST_USER
				to_list = [save_it.email , settings.EMAIL_HOST_USER]
				send_mail(subject,message,from_email,to_list)
				# to turn off errors add fail_silently = True as an arguement to send_mail
				username=form.cleaned_data.get('username');
				messages.success(request,f'Account created for {username}.')
				return redirect('register')
	else:
		form=UserRegisterForm()
	return render(request,"projects/register.html",{'form':form})
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.contrib.auth.decorators import login_required, user_passes_test
from leave.models import UserProfile,Employee,Application
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist,PermissionDenied
from django.http import HttpResponse,Http404
from django.template import RequestContext, loader
from django import forms
from django.contrib.auth import authenticate,login,logout
from leave.forms import ApplicationForm
from django.views.generic import ListView
from django.contrib import messages

#Users are divided to Depts,Clerk,'Higher'
#'higher' includes Dean,Dr,Registrar Etc
#These functions are used to verify user's groups
def isDept(user):
	return user.groups.filter(name='depts')

def isClerk(user):
	return user.groups.filter(name='clerk')

def isHigher(user):
	return user.groups.filter(name='higher')

			


# Create your views here.
def index(request):

	#Authenticate User
	if(request.method=='POST'):		#
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:  
			login(request, user)
			#Login User
	        
	   	else:

	   		return render(request, 'leave/login.html',{'message':"Invalid login !",'username':username})
	   	  	# Return an 'invalid login' error message.

	#User authenticated, Now redirect to corresponding views
	if request.user.is_authenticated():
		
		if isHigher(request.user):
			return redirect('higher')
		elif isClerk(request.user):
			return redirect('clerk')
		elif isDept(request.user):
			return redirect('dept')
		else:
			#If user do not belong to any of three groups, then it should be considered as a staff
			#Redirect this user to Admin page
			return redirect('admin:index')

	else:
		
		#Return a fresh login page
		return render(request, 'leave/login.html',{'message':""})


def logt(request):
	logout(request)
	return redirect('/')
		



@login_required
@user_passes_test(isDept)
def cancel_application(request):
	if(request.method=='POST'):
		userprofile=UserProfile.objects.get(user=request.user)
		application_id=request.POST.get('id')
		application=Application.objects.get(pk=application_id)
		



@login_required
def details(request,id):
	userprofile=UserProfile.objects.get(user=request.user)
	try:
		application=Application.objects.get(pk=id)
	except Application.DoesNotExist:
		raise Http404
	if isDept(request.user) and application.employee.dept!=userprofile.dept:
		raise PermissionDenied
	
	context= {
	'application':application,
	'days_count':(application.date_to-application.date_from).days+1
	}


	return render(request,'leave/application.html',context)



@login_required
@user_passes_test(isDept)
def sent(request):
	userprofile=UserProfile.objects.get(user=request.user)
	status = request.GET.get('status')
	if(status==None):
		status=0

	try:
		status = int(status)
	except ValueError:
		#Handle the exception
		status=0
	page = request.GET.get('page')
	all_list=Application.objects.filter(employee__dept=userprofile.dept).order_by("-time_generated")
	
	if 1<= status <=4:
		all_list= all_list.filter(status=status)
	
	paginator = Paginator(all_list, 10)
	
	try:
		applications = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		applications = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		applications = paginator.page(paginator.num_pages)


	context= {
	'name': request.user.username,
	'dept': userprofile.get_dept_display(),
	'applications':applications,
	'status' :status
	}


	return render(request,'leave/sent.html',context)






@login_required	#Require Login
@user_passes_test(isDept) #Restrict access to users from other groups 
def dept(request):
	#Information specific to the user
	userprofile=UserProfile.objects.get(user=request.user)
	context= {
	'name': request.user.username,
	'dept': userprofile.get_dept_display()
	}


	if(request.method=='POST'):
		form = ApplicationForm(userprofile.dept,request.POST,request.FILES)
		if(form.is_valid()):
			form.save()
			messages.success(request, 'Application added successfully') 
			return redirect('sent')
		else:
			context['form']=form

			return render(request,'leave/dept.html',context)


	

	form=ApplicationForm(userprofile.dept)
	
	context['form']=form

	return render(request,'leave/dept.html',context)



@login_required
@user_passes_test(isClerk)
def clerk(request):
	
	userprofile=UserProfile.objects.get(user=request.user)

	context= {
	'name': request.user.username,
	}
	return render(request,'leave/clerk.html',context)



@login_required
@user_passes_test(isHigher)
def higher(request):

	userprofile=UserProfile.objects.get(user=request.user)

	context= {
	'name': request.user.username,
	'usertype' :userprofile.get_user_type_display()
	}
	return render(request,'leave/higher.html',context)

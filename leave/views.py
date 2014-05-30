from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from leave.models import UserProfile 
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template import RequestContext, loader
from django import forms
from django.contrib.auth import authenticate,login,logout


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

	   		return render(request, 'leave/login.html',{'message':"Invalid login !"})
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



@login_required	#Require Login
@user_passes_test(isDept) #Restrict access to users from other groups 
def dept(request):
	if(request.method=='POST'):
		logout(request)
		return redirect('index')


	userprofile=UserProfile.objects.get(user=request.user)

	#Information specific to the user
	context= {
	'name': request.user.username,
	'dept': userprofile.get_dept_display()
	}

	return render(request,'leave/dept.html',context)



@login_required
@user_passes_test(isClerk)
def clerk(request):
	if(request.method=='POST'):
		logout(request)
		return redirect('index')
	

	userprofile=UserProfile.objects.get(user=request.user)

	context= {
	'name': request.user.username,
	}
	return render(request,'leave/clerk.html',context)



@login_required
@user_passes_test(isHigher)
def higher(request):
	if(request.method=='POST'):
		logout(request)
		return redirect('index')
	

	userprofile=UserProfile.objects.get(user=request.user)

	context= {
	'name': request.user.username,
	'usertype' :userprofile.get_user_type_display()
	}
	return render(request,'leave/higher.html',context)

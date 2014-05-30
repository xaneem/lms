from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from leave.models import UserProfile 
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


# Create your views here.
def index(request):
	if request.user.is_authenticated():
		try :
			user_type=UserProfile.objects.get(user=request.user).user_type

		except ObjectDoesNotExist:
			return redirect('admin:index')

		else :
			if user_type==1:
				return redirect('dept')
			elif user_type==2:
				return redirect('clerk')
			else:
				return redirect('administration')
		

   		

	else:
 		return HttpResponse("Please Login")


@login_required
def dept(request):
	return HttpResponse("Welcome to department")

@login_required
def clerk(request):
	return HttpResponse("Welcome Clerk !")

@login_required
def administration(request):
	return HttpResponse("Welcome administration!")
from django.shortcuts import render
from datetime import datetime 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.contrib.auth.decorators import login_required, user_passes_test
from leave.models import UserProfile,Employee,Application,ApplicationLog,TransactionLog
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist,PermissionDenied
from django.http import HttpResponse,Http404
from django.template import RequestContext, loader
from django import forms
from django.contrib.auth import authenticate,login,logout
from leave.forms import ApplicationForm,EmployeeEditForm,EmployeeNewForm
from django.views.generic import ListView
from django.contrib import messages
from django.core.urlresolvers import reverse
import json
from EmployeeSerializer import EmployeeSerializer
from django.core import serializers



# are divided to Depts,Clerk,'Higher'
#'higher' includes Dean,Dr,Registrar Etc
#These functions are used to verify user's groups
def isDept(user):
	return user.groups.filter(name='depts')

def isClerk(user):
	return user.groups.filter(name='clerk')

def isHigher(user):
	return user.groups.filter(name='higher')

def isDataEntry(user):
	return user.groups.filter(name="data_entry")


def getStatus(sort):
	if(sort==None):
		status=0
	elif(sort.lower()=="pending"):
		status=1
	elif(sort.lower()=="processing"):
		status=2
	elif(sort.lower()=="approved"):
		status=3
	elif(sort.lower()=="rejected"):
		status=4
	elif(sort.lower()=="cancelled"):
		status=5
	elif(sort.lower()=="all"):
		status=6
	else:
		status=0
	return status

def getApplicationsList(page,status,year,month,date):
	all_list=Application.objects.all().order_by("-time_generated")
	if 1<= status <=5 :
		all_list=all_list.filter(status=status)
	if year:
		all_list=all_list.filter(time_generated__year=year)
	print month
	if month:
		all_list=all_list.filter(time_generated__month=month)
	if date:
		all_list=all_list.filter(time_generated__day=date)
	paginator = Paginator(all_list, 10)
	
	try:
		applications = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		applications = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		applications = paginator.page(paginator.num_pages)
	return applications


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
			return redirect(reverse('higher',args=('',)))
		elif isClerk(request.user):
			return redirect(reverse('clerk',args=('',)))
		elif isDept(request.user):
			return redirect('dept')
		elif isDataEntry(request.user):
			return redirect(reverse('employees'))
		else:
			#If user do not belong to any of three groups, then it should be considered as a staff
			#Redirect this user to Admin page
			return redirect('admin:index')

	else:
		
		#Return a fresh login page
		return render(request, 'leave/login.html',{'message':""})


def logt(request):
	logout(request)
	return redirect('index')
		

@login_required
@user_passes_test(isDataEntry)
def manage_leave(request):
	if request.method=='POST':
		leave_type=request.POST.get('leave_type')
		action_type=request.POST.get('action_type')
		days=request.POST.get('count')
		leave_type=int(leave_type)
		action_type=int(action_type)
		note="Just testing"
		days=int(days)
		
		if 1<= leave_type <=2 and (action_type==-1 or action_type==1) and days>=0:
			count=0
			employees=request.POST.getlist('check[]')
			for pk in employees:
				try:
					employee=Employee.objects.get(pk=pk)
				except Employee.DoesNotExist:
					pass
				else:
					if action_type==-1 and not employee.isLeaveLeft(days,leave_type):
						pass
					else:
						employee.transaction(days,leave_type,action_type)
						TransactionLog().AdminTransaction(employee,leave_type,days,action_type,note)
						count=count+1


			if count:
				messages.success(request,"Updated "+str(count)+" employees ")
			else:
				messages.error(request,"No employee updated")
		

		else:
			messages.error(request,"Invalid Action")

		return redirect(reverse('employees'))
	else:
		raise PermissionDenied


@login_required
@user_passes_test(isDept)
def cancel_application(request):
	if request.method=='POST':
		userprofile=UserProfile.objects.get(user=request.user)
		application_id=request.POST.get('id')
		application=Application.objects.get(pk=application_id)
		if application.employee.dept==userprofile.dept and application.status==1:

			application.status=5
			application.save()
			activity="Application cancelled by "+userprofile.get_user_type_display()
			log_entry=ApplicationLog(application=application,time=datetime.now(),activity=activity)
			log_entry.save()
			messages.success(request, 'Application cancelled.')

		else:
			messages.error(request, 'Some error occured: Could not cancel application.')

		return redirect(reverse('details', args=(application.pk,)))
	else:
		raise PermissionDenied

		
@login_required
@user_passes_test(isClerk)
def start_processing(request):
	
	if(request.method=='POST'):
		userprofile=UserProfile.objects.get(user=request.user)
		user_type=userprofile.user_type
		application_id=request.POST.get('id')
		application=Application.objects.get(pk=application_id)
		to_json={}
		notes=request.POST.get('notes',"")
				
		if application.status==1 and isClerk(request.user):
				
			application.status=2
			application.save()
			activity="Processing started "
			log_entry=ApplicationLog(application=application,time=datetime.now(),activity=activity,notes=notes)
			log_entry.save()
			to_json['result']=1
			to_json['message']='Application marked as processing'
			messages.success(request, 'Application marked as processing')
		else:
			to_json['result']=0
			to_json['message']='error'
			messages.error(request,'Error: Could not change status. Try again.')
		return HttpResponse(json.dumps(to_json), mimetype='application/json')
	else:
		raise PermissionDenied

@login_required
def print_application(request,id):
	try:
		application=Application.objects.get(pk=id)
	except Application.DoesNotExist:
		raise Http404
	employee=application.employee
	log=TransactionLog.objects.filter(time__lt=application.time_received,employee=employee).order_by("-time")[:5]
	context={
	'application':application,
	'days_count':(application.date_to-application.date_from).days+1,
	'log':log
	}
	return render(request,'leave/print.html',context)




@login_required
@user_passes_test(isHigher)
def complete(request):
	if(request.method=='POST'):
		userprofile=UserProfile.objects.get(user=request.user)
		application_id=request.POST.get('id')
		status=request.POST.get('status')
		status=int(status)
		date_from=request.POST.get('date_from',"")
		date_to=request.POST.get('date_to',"")
		notes=request.POST.get('notes',"")
		application=Application.objects.get(pk=application_id)
		employee=application.employee
		to_json = {}
		valid=True

		try:
			print date_to
			print date_from
			date_to=datetime.strptime(date_to, "%m/%d/%Y").date()
			date_from=datetime.strptime(date_from, "%m/%d/%Y").date()
			print date_to
			print date_from
			

		except ValueError:
			valid=False
			to_json['message']='Invalid dates entered.'
		else:
			if date_from>date_to or date_to>application.new_date_to or date_from<application.new_date_from:
				valid=False
				to_json['message']='Selected dates out of range. Please select valid dates.'
		if not valid:
			to_json['result']=0
			messages.error(request, to_json['message'])
			return HttpResponse(json.dumps(to_json), mimetype='application/json')

		if application.status== 2 and 3 <= status <= 4:
			days=(date_to-date_from).days+1

			if status==4 or employee.isLeaveLeft(days,application.leave_type):
				application.status=status
				application.time_approved=datetime.now()
				if status==3 and (application.new_date_from!=date_from or application.new_date_to!=date_to):
					if notes and notes!="":
						notes+='\n'
					notes+=userprofile.get_user_type_display()+" updated  date  : "+str(date_from)+" to "+str(date_to)
				if status==3:
					application.new_date_from=date_from
					application.new_date_to=date_to
					employee.transaction(days,application.leave_type,-1)
					
				application.save()
				if application.status==3:
					TransactionLog().ApplicationTransaction(employee,application)

				activity="Application "+application.get_status_display()
				log_entry=ApplicationLog(application=application,time=datetime.now(),activity=activity,notes=notes)
				log_entry.save()
				messages.success(request, 'Application '+application.get_status_display()+' successfully')
				
				to_json['result']=1
				to_json['message']='Application '+application.get_status_display()+' successfully'
    
				
				
			else:
				to_json['result']=0
				to_json['message']="Insufficient number of leaves left!"
				messages.error(request, 'Insufficient number of leaves left!')



		else:
			to_json['result']=0
			to_json['message']='Some error occured. Please try again'
		return HttpResponse(json.dumps(to_json), mimetype='application/json')
	else:
		raise PermissionDenied


@login_required
def details(request,id):
	userprofile=UserProfile.objects.get(user=request.user)
	try:
		application=Application.objects.get(pk=id)
	except Application.DoesNotExist:
		raise Http404
	if isDept(request.user) and application.employee.dept!=userprofile.dept:
		raise PermissionDenied
	if isClerk(request.user) and not application.time_received:
		application.time_received=datetime.now()
		application.save()
		activity="Application Received at Est.Office"
		log_entry=ApplicationLog(application=application,time=datetime.now(),activity=activity)
		log_entry.save()

	application_log=ApplicationLog.objects.filter(application=application).order_by("time")
							

	context= {
	'name':request.user.username,
	'application':application,
	'days_count':(application.date_to-application.date_from).days+1,
	'user_type':userprofile.user_type,
	'user_display_name':userprofile.get_user_type_display,
	'dept': userprofile.get_dept_display,
	'application_log':application_log
	}
	return render(request,'leave/application.html',context)





@login_required
def employee(request,id):
	userprofile=UserProfile.objects.get(user=request.user)
	page=request.GET.get('page')
	try:
		employee=Employee.objects.get(pk=id)
	except Employee.DoesNotExist:
		raise Http404
	if isDept(request.user) and employee.dept!=userprofile.dept:
		raise PermissionDenied
	all_list=TransactionLog.objects.filter(employee=employee).order_by("-time")

	paginator = Paginator(all_list, 10)
	
	try:
		transaction_log = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		transaction_log = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		transaction_log = paginator.page(paginator.num_pages)

	context= {
	'name':request.user.username,
	'employee':employee,
	'user_type':userprofile.user_type,
	'user_display_name':userprofile.get_user_type_display,
	'dept': userprofile.get_dept_display,
	'transaction_log': transaction_log
	}

	return render(request,'leave/employee.html',context)

@login_required
@user_passes_test(isDataEntry)
def edit_employee(request,id):
	try:
		employee=Employee.objects.get(pk=id)
	except Employee.DoesNotExist:
		raise Http404

	form=EmployeeEditForm(instance=employee)
	
	context={
	'form':form
	}
	if request.method=='POST':
		form = EmployeeEditForm(request.POST,instance=employee)
		if form.is_valid():
			form.save()
			messages.success(request, 'Employee details updated')
			context['form']=EmployeeEditForm(instance=employee)
		else:
			messages.error(request,'Please correct incorrect fields')
			context['form']=form
		return render(request,'leave/edit_employee.html',context)
	
	else:	
		return render(request,'leave/edit_employee.html',context)

@login_required
@user_passes_test(isDataEntry)
def new_employee(request):
	context={
	}
	if request.method=='POST':
		form = EmployeeNewForm(request.POST)
		code=form.data['code']
		print code
		try:
			employee=Employee.objects.filter(is_active=False).get(code=code)
			messages.success(request, 'Employee code already exists ,Please update details Here')
			return redirect(reverse('edit_employee',args=(employee.pk,)))
		except Employee.DoesNotExist:
			if form.is_valid():
				
					new_employee=form.save()
					employee=Employee.objects.get(code=form.cleaned_data['code'])
					note="Entering existing data"
	   				TransactionLog().AdminTransaction(employee,1,employee.earned_balance,1,note)
	   				TransactionLog().AdminTransaction(employee,2,employee.hp_balance,1,note)
					messages.success(request, 'New Employee Added')
					return(redirect(reverse('employees')))
			else:
				messages.error(request,'Please correct incorrect fields')
				context['form']=form
		return render(request,'leave/new_employee.html',context)
	
	
	else:	
		context['form']=EmployeeNewForm()
		return render(request,'leave/new_employee.html',context)



@login_required
@user_passes_test(isDataEntry)
def employees(request):
	employees=Employee.objects.filter(is_active=True)
	serializer = EmployeeSerializer()
	serialized_employees = serializer.serialize(employees)
	print serialized_employees
	context={
	'employees':serialized_employees
	}
	
	return render(request,'leave/employees.html',context)


@login_required
@user_passes_test(isDept)
def sent(request,sort,year,month,date):
	userprofile=UserProfile.objects.get(user=request.user)
	status=getStatus(sort)
	page = request.GET.get('page')
	applications=getApplicationsList(page,status,year,month,date)

	context= {
	'name': request.user.username,
	'dept': userprofile.get_dept_display(),
	'applications':applications,
	'status' :status,
	'user_type': userprofile.user_type,
	}

	return render(request,'leave/sent.html',context)


@login_required	#Require Login
@user_passes_test(isDept) #Restrict access to users from other groups 
def dept(request):
	#Information specific to the user
	userprofile=UserProfile.objects.get(user=request.user)
	context= {
	'name': request.user.username,
	'dept': userprofile.get_dept_display(),
	'user_type': userprofile.user_type
	}


	if(request.method=='POST'):
		form = ApplicationForm(userprofile.dept,request.POST,request.FILES)
		if(form.is_valid()):
			new_application=form.save()
			new_application.new_date_from=new_application.date_from
			new_application.new_date_to=new_application.date_to
			new_application.save()
			activity="Application generated by "+userprofile.get_user_type_display()
			log_entry=ApplicationLog(application=new_application,time=datetime.now(),activity=activity)
			log_entry.save()
			messages.success(request, 'Application added successfully')
			return redirect(reverse('details', args=(new_application.pk,)))
		else:
			context['form']=form

			return render(request,'leave/dept.html',context)


	else:
		form=ApplicationForm(userprofile.dept)
		context['form']=form
		return render(request,'leave/dept.html',context)



@login_required
@user_passes_test(isClerk)
def clerk(request,sort,year,month,date):
	userprofile=request.user.userprofile
	status=getStatus(sort)
	if status==0:
		status=1
	page = request.GET.get('page')
	applications=getApplicationsList(page,status,year,month,date)
	context= {
	'name': request.user.username,
	'applications':applications,
	'status' :status,
	'user_type': userprofile.user_type,
	}

	return render(request,'leave/clerk.html',context)



@login_required
@user_passes_test(isHigher)
def higher(request,sort,year,month,date):

	page=request.GET.get('page')
	userprofile=UserProfile.objects.get(user=request.user)
	status=getStatus(sort)
	if not sort or status==0:
		sort=''

	if status == 0 :
		status = 2

	

	url=reverse('higher', args=(sort,))
	
	if not sort=='':
		url=url+'/'
	
			
		
	
	applications=getApplicationsList(page,status,year,month,date)
	context= {
	'name': request.user.username,
	'applications': applications,
	'status': status,
	'user_type': userprofile.user_type,
	'current_url': url
	}
	return render(request,'leave/higher.html',context)


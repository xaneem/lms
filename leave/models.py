from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from CustomFileField import CustomFileField

# Each choice in this list represents a End-User of the software,
# who has the previlege to enter a new application to the system.


#Types of leave
LEAVE_TYPES = (
	#(1,'Special Casual Leave'),
	(1,'Earned Leave'),
	(2,'Half Pay Leave'),
	(3,'Commuted Leave'),
	#(3,'On Duty Leave'),
	)



#Different types of users
USER_TYPES = (
	(0, ''),
	(1,	'Section Head'),
    (2, 'Est. Office'),
    (4, 'Deputy Registrar'),
    (5, 'Data Admin')
)


#Status of Application
STATUS = (
	(0,'Deleted'),
	(1,'Pending'),
	(2,'Processing'),
	(3,'Approved'),
	(4,'Rejected'),
	(5,'Cancelled')
	)

class Department(models.Model):
	name = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name

#Model for employees
class Employee(models.Model):
		
	code = models.CharField(max_length=10,null=True,unique=True)
	name = models.CharField(max_length=100)
	dept = models.ForeignKey('Department')
	earned_balance = models.IntegerField(default=0)
	hp_balance = models.IntegerField(default=0)
	email = models.EmailField(max_length=75)
	is_active= models.BooleanField(default=True)

	def __unicode__(self):
		return self.code+" : "+self.name

	def isLeaveLeft(self,days,leave_type):
		if leave_type==1:
			return days<=self.earned_balance
		elif leave_type==2:
			return days<=self.hp_balance
		elif leave_type==3:
			return days*2<=self.hp_balance
		else:
			return False

	def approveTransaction(self,days,leave_type,action_type):
		earned_change=0
		hp_change=0
		if leave_type==1:
			earned_change+=days*action_type
		elif leave_type==2:
			hp_change+=days*action_type
		elif leave_type==3:
			hp_change+=2*days*action_type
		self.transaction(hp_change,earned_change);
		return True

	def transaction(self,hp_change,earned_change):
		self.earned_balance+=earned_change
		self.hp_balance+=hp_change
		self.save()
		return True

class EmployeeUpdateLog(models.Model):
	action=models.OneToOneField('Action',related_name='update_log')
	employee=models.ForeignKey('Employee')
	is_new=models.BooleanField(default=False)
	new_name = models.CharField(max_length=100)
	new_dept = models.ForeignKey('Department',related_name='update_new_dept')
	new_email = models.EmailField(max_length=75)
	new_is_active= models.BooleanField(default=True)
	old_name = models.CharField(max_length=100)
	old_dept = models.ForeignKey('Department',related_name='update_old_dept')
	old_email = models.EmailField(max_length=75)
	old_is_active= models.BooleanField(default=True)
	


#Model to represent different types of users 
class UserProfile(models.Model):

	user = models.OneToOneField(User)
	user_type = models.IntegerField(choices=USER_TYPES)
	dept = models.ForeignKey('Department')
	

class Action(models.Model):
	count=models.IntegerField(default=0)
	is_leave=models.BooleanField(default=True)
	note=models.TextField(max_length=100,blank=True,null=True)
	status=models.IntegerField(choices=STATUS,default=1)
	time_generated=models.DateTimeField(auto_now_add=True)
	time_approved=models.DateTimeField(null=True)
	reply_note=models.TextField(max_length=100,blank=True,null=True)

	

class ApplicationLog(models.Model):
	application=models.ForeignKey('Application')
	time = models.DateTimeField()
	activity= models.TextField(max_length=100,blank=True,null=True)
	notes=models.TextField(max_length=100,blank=True,null=True)


class TransactionLog(models.Model):
	employee=models.ForeignKey('Employee')
	action=models.ForeignKey('Action',null=True)
	application=models.ForeignKey('Application',null=True)
	is_admin=models.BooleanField(default=False)
	earned_balance=models.IntegerField()
	earned_change=models.IntegerField(default=0)
	hp_balance=models.IntegerField()
	hp_change=models.IntegerField(default=0)
	note=models.TextField(max_length=100,blank=True,null=True)
	time= models.DateTimeField(null=True)


	def toText(self):
		change=0
		text=""
		
		if self.hp_change:
			change=self.hp_change
			text+=str(abs(change))+" Halfpay leave "
		elif self.earned_change:
			change=self.earned_change
			text+=str(abs(change))+" Earned leave "

		if change<0:
			text+="Debit "
		elif change>0:
			text+="Credit "
		elif change==0:
			return "No changes in leave balance"

		return text

	def ApplicationTransaction(self,employee,application):
		earned_balance=employee.earned_balance
		hp_balance=employee.hp_balance
		earned_change=0
		hp_change=0
		if application.is_credit:
			if application.is_new:
				action_type=1
			else :
				action_type=-1
		else:
			if application.is_new:
				action_type=-1
			else :
				action_type=1

		if application.is_credit:
			days=application.days
		else:
			days=(application.new_date_to-application.new_date_from).days+1

		if application.leave_type==1:
			earned_change+=days*action_type
		elif application.leave_type==2:
			hp_change+=days*action_type
		elif application.leave_type==3:
			hp_change+=2*days*action_type
			

		self.employee=employee
		self.application=application
		self.earned_balance=earned_balance
		self.earned_change=earned_change
		self.hp_balance=hp_balance
		self.hp_change=hp_change
		self.time=datetime.now()
		self.save()

	def AdminTransaction(self,action,employee,leave_type,days,action_type,note):
		earned_balance=employee.earned_balance
		hp_balance=employee.hp_balance
		earned_change=0
		hp_change=0
		if leave_type==1:
			earned_change+=days*action_type
		elif leave_type==2:
			hp_change+=days*action_type
		elif leave_type==3:
			hp_change+=days*2*action_type
		self.action=action
		print action
		self.employee=employee
		self.leave_type=leave_type
		self.is_admin=True
		self.earned_balance=earned_balance
		self.earned_change=earned_change
		self.hp_balance=hp_balance
		self.hp_change=hp_change
		self.time=datetime.now()
		self.note=note
		self.save()
	
	



#Model to represent an individual application
class Application(models.Model):

	employee = models.ForeignKey('Employee')
	is_new = models.BooleanField(default=True)
	is_credit= models.BooleanField(default=False)
	original= models.ForeignKey('self',null=True)
	# Original field of New applications refers to ongoing cancel request for the same
	leave_type = models.IntegerField(choices=LEAVE_TYPES)
	date_from = models.DateField(null=True)
	date_to	= models.DateField(null=True)
	days=models.IntegerField(default=0)
	status = models.IntegerField(choices=STATUS,default=1)
	reason = models.TextField(max_length=200)
	new_date_to=models.DateField(null=True)
	new_date_from=models.DateField(null=True)
	attachment1= CustomFileField(upload_to='.',null=True,blank=True)
	attachment2= CustomFileField(upload_to='.',null=True,blank=True)
	attachment3= CustomFileField(upload_to='.',null=True,blank=True)
	time_generated = models.DateTimeField(auto_now_add=True)
	time_received = models.DateTimeField(null=True)
	time_approved = models.DateTimeField(null=True,blank=True)
	#This field will be set only when the application is approved/rejected	
	

	def __unicode__(self):
		return self.employee.name + " - " + self.get_leave_type_display()	

	def toText(self):
		text=""
		if self.is_new and not self.is_credit:
			text+="New "+self.get_leave_type_display()+" "
		elif self.is_new and self.is_credit:
			text+="Credit "+self.get_leave_type_display()+" "

		else:
			text+="Cancel Approved Leave"
		
		return text





	def CancelRequest(self,reason,attachment1,attachment2,attachment3):
		cancel_application=Application(original=self,is_new=False,
		employee=self.employee,leave_type=self.leave_type,date_from=self.new_date_from,
		date_to=self.new_date_to,new_date_from=self.new_date_from,
		new_date_to=self.new_date_to,reason=reason,attachment1=attachment1,
		attachment2=attachment2,attachment3=attachment3,)
		cancel_application.save()
		self.original=cancel_application
		# Original field of New applications refers to ongoing cancel request for the same
		self.save()
		return cancel_application
















	



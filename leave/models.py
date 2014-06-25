from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Each choice in this list represents a End-User of the software,
# who has the previlege to enter a new application to the system.
DEPARTMENTS = (
	(0,'Other'),
	(1,'Computer Science'),
	(2,'Mechanical'),
	(3,'Electrical'),
	(4,'Civil'),
	(5,'Electronics'),
	(6,'Chemical'),
	(7,'Biotechnology'),
	(8,'Architecture'),
	(9,'Mathematics'),
	(10,'Nanotechnology'),
	(11,'Chemistry'),
	(12,'SOMS'),
	)

#Different posts of Employees
POSTS = (
	(1,'Ad-Hoc'),
	(2,'Assistant Professor'),
	(3,'Associate Professor'),
	(4,'HOD'),
	(5,'Professor'),
	)


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
    (5, 'Data Entry')
   
)


#Status of Application
STATUS = (
	(1,'Pending'),
	(2,'Processing'),
	(3,'Approved'),
	(4,'Rejected'),
	(5,'Cancelled')
	)


#Model for employees
class Employee(models.Model):
		
	code = models.CharField(max_length=10,null=True,unique=True)
	name = models.CharField(max_length=100)
	dept = models.IntegerField(choices=DEPARTMENTS)
	earned_balance = models.IntegerField(default=0)
	hp_balance = models.IntegerField(default=0)
	post = models.IntegerField(choices=POSTS)
	email = models.EmailField(max_length=75)
	is_active= models.BooleanField(default=True)

	def __unicode__(self):
		return self.name

	def isLeaveLeft(self,days,leave_type):
		if leave_type==1:
			return days<=self.earned_balance
		elif leave_type==2:
			return days<=self.hp_balance
		elif leave_type==3:
			return days*2<=self.hp_balance
		else:
			return False

	def transaction(self,days,leave_type,action_type):
		if leave_type==1:
			self.earned_balance+=days*action_type
		elif leave_type==2:
			self.hp_balance+=days*action_type
		elif leave_type==3:
			self.hp_balance+=2*days*action_type
		else:
			return False
		self.save()
		return True




#Model to represent different types of users 
class UserProfile(models.Model):

	user = models.OneToOneField(User)
	user_type = models.IntegerField(choices=USER_TYPES)
	dept = models.IntegerField(choices=DEPARTMENTS, default=0)
	
	

class ApplicationLog(models.Model):
	application=models.ForeignKey('Application')
	time = models.DateTimeField()
	activity= models.TextField(max_length=100,blank=True,null=True)
	notes=models.TextField(max_length=100,blank=True,null=True)


class TransactionLog(models.Model):
	employee=models.ForeignKey('Employee')
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
			text+=str(abs(change))+" Halfpay leave"
		elif self.earned_change:
			change=self.earned_change
			text+=str(abs(change))+" Earned leave"
		if change<0:
			text+=" debited by"
		elif change>0:
			text+=" credited by"

		if not self.is_admin:
			text+=" Application #"+str(self.application.pk)
		else:
			text+=" Admin"
		return text

	def ApplicationTransaction(self,employee,application):
		earned_balance=employee.earned_balance
		hp_balance=employee.hp_balance
		earned_change=0
		hp_change=0
		days=(application.new_date_to-application.new_date_from).days+1
		if application.leave_type==1:
			earned_change-=days
		elif application.leave_type==2:
			hp_change-=days
		elif application.leave_type==3:
			hp_change-=2*days

		self.employee=employee
		self.application=application
		self.earned_balance=earned_balance
		self.earned_change=earned_change
		self.hp_balance=hp_balance
		self.hp_change=hp_change
		self.time=datetime.now()
		self.save()

	def AdminTransaction(self,employee,leave_type,days,action_type,note):
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
	original= models.ForeignKey('self',null=True)
	leave_type = models.IntegerField(choices=LEAVE_TYPES)
	date_from = models.DateField()
	date_to	= models.DateField()
	status = models.IntegerField(choices=STATUS,default=1)
	reason = models.TextField(max_length=200)
	new_date_to=models.DateField(null=True)
	new_date_from=models.DateField(null=True)
	attachment1 = models.FileField(upload_to=".",null=True,blank=True)
	attachment2 = models.FileField(upload_to=".",null=True,blank=True)
	attachment3 = models.FileField(upload_to=".",null=True,blank=True)
	time_generated = models.DateTimeField(auto_now_add=True)
	time_received = models.DateTimeField(null=True)
	time_approved = models.DateTimeField(null=True,blank=True)
	#This field will be set only when the application is approved/rejected	
		
	def __unicode__(self):
		return self.employee.name + " - " + self.get_leave_type_display()	















	



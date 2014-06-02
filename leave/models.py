from django.db import models
from django.contrib.auth.models import User


# Each choice in this list represents a End-User of the software,
# who has the previlege to enter a new application to the system.
DEPARTMENTS = (
	(0,'OTHER'),
	(1,'CSED'),
	(2,'MED'),
	(3,'EED'),
	(4,'CED'),

	)


#Different posts of Employees
POSTS = (
	(1,'AD-HOC'),
	(2,'ASSISTANT PROFESSOR'),
	(3,'ASSOCIATE PROFESSOR'),
	(4,'HOD'),
	)


#Types of leave
LEAVE_TYPES = (
	(1,'HALF PAY'),
	(2,'ON DUTY'),
	(3,'EARNED LEAVE'),
	)



#Different types of users
USER_TYPES = (
	(1,	'HOD'),
    (2, 'CLERK'),
    (3, 'DEAN'),
    (4, 'DR'),
    (5,	'REGISTRAR'),
    (6,	'DIRECTOR'),
)


#Status of Application
STATUS = (
	(1,'PENDING'),
	(2,'PROCESSING'),
	(3,'APPROVED')
	)


# Create your models here.


#Model for employees
class Employee(models.Model):
		
	code = models.CharField(max_length=10,null=True)
	name = models.CharField(max_length=100)
	dept = models.IntegerField(choices=DEPARTMENTS)
	leave_balance = models.IntegerField();
	post = models.IntegerField(choices=POSTS)
	email = models.EmailField(max_length=75)
	
	def __unicode__(self):
		return self.name






#Model to represent different types of users 
class UserProfile(models.Model):

	user = models.OneToOneField(User)
	user_type = models.IntegerField(choices=USER_TYPES)
	dept = models.IntegerField(choices=DEPARTMENTS, default=0)
	
	





#Model to represent an individual application
class Application(models.Model):

	employee = models.ForeignKey('Employee')
	leave_type = models.IntegerField(choices=LEAVE_TYPES)
	date_from = models.DateField()
	date_to	= models.DateField()
	status = models.IntegerField(choices=STATUS,default=1)
	current_position= models.IntegerField(choices=USER_TYPES,default=1)

	reason = models.TextField(max_length=200)
	attachment1 = models.FileField(upload_to="/home/",null=True)
	attachment2 = models.FileField(upload_to="/home/",null=True)
	attachment3 = models.FileField(upload_to="/home/",null=True)
	time_generated = models.DateTimeField(auto_now_add=True)
	time_apporoved = models.DateTimeField(null=True,blank=True)	#This field will be set only when the application is received.
	
	
	def __unicode__(self):
		return self.employee.name+self.get_leave_type_display()	



#Model to represent a cancel request , Each entry references a leave application
class CancelRequest(models.Model):

	application = models.ForeignKey('Application')
	reason = models.CharField(max_length=200)
	date_from = models.DateField()
	date_to	= models.DateField()
	status = models.IntegerField(choices=STATUS)
	current_position = models.IntegerField(choices=USER_TYPES)
	time_generated = models.DateTimeField()
	time_apporoved = models.DateTimeField(null=True,blank=True)















	



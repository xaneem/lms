from django.db import models
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
	(1,'Special Casual Leave'),
	(2,'Earned Leave'),
	(3,'Half Pay Leave'),
	(3,'Commuted Leave'),
	(3,'On Duty Leave'),
	)



#Different types of users
USER_TYPES = (
	(0, ''),
	(1,	'Section Head'),
    (2, 'Est. Office'),
    (4, 'Deputy Registrar'),
   
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
	
	

class ApplicationLog(models.Model):
	application=models.ForeignKey('Application')
	time = models.DateTimeField()
	activity= models.TextField(max_length=100,blank=True,null=True)
	notes=models.TextField(max_length=100,blank=True,null=True)




#Model to represent an individual application
class Application(models.Model):

	employee = models.ForeignKey('Employee')
	leave_type = models.IntegerField(choices=LEAVE_TYPES)
	date_from = models.DateField()
	date_to	= models.DateField()
	status = models.IntegerField(choices=STATUS,default=2)
	current_position= models.IntegerField(choices=USER_TYPES,default=4)
	reason = models.TextField(max_length=200)
	new_date_to=models.DateField(null=True)
	new_date_from=models.DateField(null=True)
	attachment1 = models.FileField(upload_to=".",null=True,blank=True)
	attachment2 = models.FileField(upload_to=".",null=True,blank=True)
	attachment3 = models.FileField(upload_to=".",null=True,blank=True)
	time_generated = models.DateTimeField(auto_now_add=True)
	time_approved = models.DateTimeField(null=True,blank=True)	#This field will be set only when the application is received.
		
	def __unicode__(self):
		return self.employee.name + " - " + self.get_leave_type_display()	



#Model to represent a cancel request , Each entry references a leave application
class CancelRequest(models.Model):

	application = models.ForeignKey('Application')
	reason = models.CharField(max_length=200)
	date_from = models.DateField()
	date_to	= models.DateField()
	status = models.IntegerField(choices=STATUS)
	current_position = models.IntegerField(choices=USER_TYPES)
	time_generated = models.DateTimeField()
	time_approved = models.DateTimeField(null=True,blank=True)















	



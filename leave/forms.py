from django.forms import ModelForm
from leave.models import Application,Employee


class ApplicationForm(ModelForm):
	class Meta:
   		model = Application
   		fields = ['employee', 'leave_type', 'date_from', 'date_to','reason','attachments']
	 



from django.forms import ModelForm
from datetime import datetime 
from leave.models import Application,Employee


class ApplicationForm(ModelForm):
	class Meta:
   		model = Application
   		fields = ['employee', 'leave_type', 'date_from', 'date_to','reason','attachments']
	
	def is_valid(self):
		valid=super(ApplicationForm,self).is_valid()
		if not valid:
			return valid

		date_from=self.cleaned_data['date_from']
		date_to=self.cleaned_data['date_to']
		leave_balance=self.cleaned_data['employee'].leave_balance
		if date_from<datetime.now().date():
			self._errors['date_from']="Aaha?"
			return False

		if(date_to<date_from):
			self._errors['date_to']="Seriously? :P"
			return False

		

		if((date_to-date_from).days>leave_balance):
			self._errors['date_to']="Insufficient leave balance"
			return False


		return True







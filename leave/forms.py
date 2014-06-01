from django.forms import ModelForm
from leave.models import Application


class ApplicationForm(ModelForm):

	def __init__(self, dept, **kwargs):
        self._user = kwargs.pop('user')
        super(MyForm, self).__init__(*args, **kwargs)

   	class Meta:
   		model = Application
   		fields = ['employee', 'leave_type', 'date_from', 'date_to','reason','attachments']



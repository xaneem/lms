from django.core.serializers.json import Serializer
from django.core.urlresolvers import reverse

class EmployeeSerializer(Serializer):
    def get_dump_object(self, obj):
    	self._current['pk']=obj.pk
    	self._current['dept_value'] = obj.dept.pk
        self._current['dept'] = obj.dept.name
        self._current['edit_url'] = reverse('edit_employee',args=(obj.pk,))
        return self._current

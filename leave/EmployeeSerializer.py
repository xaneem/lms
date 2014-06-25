from django.core.serializers.json import Serializer
from django.core.urlresolvers import reverse

class EmployeeSerializer(Serializer):
    def get_dump_object(self, obj):
    	self._current['dept_value'] = obj.dept
    	self._current['post_value'] = obj.post
        self._current['dept'] = obj.get_dept_display()
        self._current['post'] = obj.get_post_display()
        self._current['edit_url'] = reverse('edit_employee',args=(obj.pk,))
        return self._current

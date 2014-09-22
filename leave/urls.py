from django.conf.urls import patterns, url
from django.conf import settings

from leave import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),  
    url(r'^dept/$', views.dept, name='dept'),
    url(r'^new/([a-zA-Z]+)?$', views.new_application, name='new_application'),
    url(r'^history/([a-zA-Z]+)?/?([0-9]{4})?-?([0-9]{2})?-?([0-9]{2})?', views.sent, name='sent'),
    url(r'^applications/([a-zA-Z]+)?/?([0-9]{4})?-?([0-9]{2})?-?([0-9]{2})?', views.applications,name='applications'),
    url(r'^logt/',views.logt,name='logt'),
    url(r'^application/(\d+)/print$',views.print_application,name='print'),
    url(r'^application/(\d+)/cancel$',views.cancel,name='cancel'),
    url(r'^action/(\d+)/$',views.action,name='action'),
    url(r'^actions/([a-zA-Z]+)?$',views.actions,name='actions'),
    url(r'^manage_action/$',views.manage_action,name='manage_action'),
    url(r'^action_history/([a-zA-Z]+)?$',views.action_history,name='action_history'),
    url(r'^employee/(\d+)/$',views.employee,name='employee'),
    url(r'^employees/$',views.employees,name='employees'),
    url(r'^select_employee/$',views.select_employee,name='select_employee'),
    url(r'^employee/(\d+)/edit$',views.edit_employee,name='edit_employee'),
    url(r'^employee/new$',views.new_employee,name='new_employee'),
    url(r'^application/(\d+)/$',views.details,name='details'),
    url(r'^manage_leave/$',views.manage_leave,name='manage_leave'),
    url(r'^delete_application/$',views.delete_application,name='delete_application'),
    url(r'^start_processing/$',views.start_processing,name='start_processing'),
    url(r'^complete/$',views.complete,name='complete'),
    url(r'^user_guide/$', views.user_guide,name='user_guide'),
 	url(r'^attachments/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }))
 
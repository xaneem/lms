from django.conf.urls import patterns, url
from django.conf import settings

from leave import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),  
    url(r'^dept/$', views.dept, name='dept'),
    url(r'^dept/sent/([a-zA-Z]+)?/?([0-9]{4})?-?([0-9]{2})?-?([0-9]{2})?', views.sent, name='sent'),
    url(r'^higher/([a-zA-Z]+)?/?([0-9]{4})?-?([0-9]{2})?-?([0-9]{2})?', views.higher,name='higher'),
    url(r'^clerk/([a-zA-Z]+)?/?([0-9]{4})?-?([0-9]{2})?-?([0-9]{2})?', views.clerk,name='clerk'),
    url(r'^logt/',views.logt,name='logt'),
    url(r'^print/(\d+)/$',views.print_application,name='print'),
    url(r'^details/(\d+)/$',views.details,name='details'),
    url(r'^cancel_application/$',views.cancel_application,name='cancel_application'),
    url(r'^start_processing/$',views.start_processing,name='start_processing'),
    url(r'^complete/$',views.complete,name='complete'),
 	url(r'^attachments/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }))
 
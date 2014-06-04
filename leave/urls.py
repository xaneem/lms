from django.conf.urls import patterns, url
from django.conf import settings

from leave import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^dept/sent', views.sent, name='sent'),
    url(r'^dept/', views.dept, name='dept'),
    url(r'^clerk/', views.clerk, name='clerk'),
    url(r'^higher/',views.higher,name='higher'),
    url(r'^logt/',views.logt,name='logt'),
    url(r'^details/(\d+)/$',views.details,name='details'),
    url(r'^cancel_application/$',views.cancel_application,name='cancel_application'),
 	url(r'^attachments/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }))
 
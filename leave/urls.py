from django.conf.urls import patterns, url

from leave import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^dept/sent', views.sent, name='sent'),
    url(r'^dept/', views.dept, name='dept'),
    url(r'^clerk/', views.clerk, name='clerk'),
    url(r'^higher/',views.higher,name='higher'),
    url(r'^logt/',views.logt,name='logt'))

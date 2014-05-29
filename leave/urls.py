from django.conf.urls import patterns, url

from leave import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
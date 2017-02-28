from django.conf.urls import url

from . import views

app_name = 'test_app'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^authorized/$', views.authorized, name='authorized'),
    url(r'^viewDestinations/$', views.view_destinations, name='view_destinations'),
]
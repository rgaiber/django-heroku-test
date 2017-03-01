from django.conf.urls import url

from . import views

app_name = 'test_app'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^authorized/$', views.authorized, name='authorized'),
    url(r'^viewDestinations/$', views.view_destinations, name='view_destinations'),
    url(r'^viewPhotos/(?P<destination_id>[0-9]+)/(?P<destination_name>[\w\- ]+)/?', views.view_photos, name='view_photos')
]
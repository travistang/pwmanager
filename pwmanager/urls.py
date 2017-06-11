from django.conf.urls import url

from . import views

urlpatterns = [
 
    url(r'^create$',views.create,name = 'create'),
    url(r'^remove$',views.remove,name = 'remove'),
    url(r'^add_device_request$',views.request_code,name = 'request_code'),
    url(r'^authorize/(?P<code>\w{256})/$',views.authorize,name = 'authorize'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^register/$',views.register,name = 'register'),
    url(r'^authenticate/$',views.authenticate,name = 'authenticate'),
    url(r'^$', views.index, name='index')
]
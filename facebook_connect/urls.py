from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from registration.views import register

urlpatterns = patterns('',
    url(r'^register/$',
        register,
        { 'backend': 'facebook_connect.FacebookConnectBackend' },
        name='facebook_register'),
    url(r'^facebook/xd_receiver.html$',
        'django.views.generic.simple.direct_to_template',
        { 'template':'xd_receiver.html' },
        name='facebook_xd_receiver'),
    url(r'^login/$',
        'facebook_connect.views.facebook_login',
        name='facebook_login'),
)
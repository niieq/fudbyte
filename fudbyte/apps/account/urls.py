__author__ = 'nii'
from django.conf.urls import url
from .views import register, login, logout, process_reset_password

urlpatterns = [
    url(r'^register/$', register, name='create'),
    url(r'^login/$', login, name='login'),
    # url(r'^recover/$', recover_password_request, name='recover'),
    url(r'^recover_process/(?P<url_token>[-\w]+)/$', process_reset_password, name='process_recover'),
    url(r'^logout/$', logout, name='logout'),
]
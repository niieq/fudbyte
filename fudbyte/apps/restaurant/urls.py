from django.conf.urls import url
from .views import restaurant_timeline


urlpatterns = [
    url(r'^(?P<restaurant_slug>[-\w]+)/timeline$', restaurant_timeline, name='timeline'),
]
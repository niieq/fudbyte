from django.conf.urls import url
from .views import restaurant_timeline, post_food_comment, foods


urlpatterns = [
    url(r'^(?P<restaurant_slug>[-\w]+)/timeline$', restaurant_timeline, name='timeline'),
    url(r'^(?P<restaurant_slug>[-\w]+)/foods$', foods, name='restaurant_food'),
    url(r'^(?P<restaurant_slug>[-\w]+)/(?P<food_slug>[-\w]+)/write_comment$', post_food_comment, name='write_comment'),
]
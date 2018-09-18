from django.conf.urls import url
from .views import index, food_detail, post_food_comment


urlpatterns = [
    url(r'^$', index),
    url(r'^food/(?P<food_slug>\w+)$', food_detail),
    url(r'^food/(?P<food_slug>\w+)/add_comment$', post_food_comment)
]
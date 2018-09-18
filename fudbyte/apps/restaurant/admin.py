from django.contrib import admin
from .models import Restaurant, Food, Comment

admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(Comment)
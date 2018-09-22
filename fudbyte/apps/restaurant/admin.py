from django.contrib import admin
from .models import Restaurant, Food, Comment


class FoodAdmin(admin.ModelAdmin):

    list_display = ('name', 'restaurant', 'image')
    search_fields = ('name', 'restaurant__name')

admin.site.register(Restaurant)
admin.site.register(Food, FoodAdmin)
admin.site.register(Comment)
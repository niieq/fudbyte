from django.contrib import admin
from .models import Restaurant, Food, Comment, FoodLike, RestaurantUser


class FoodAdmin(admin.ModelAdmin):

    list_display = ('name', 'restaurant', 'image')
    search_fields = ('name', 'restaurant__name')

admin.site.register(Restaurant)
admin.site.register(Food, FoodAdmin)
admin.site.register(Comment)
admin.site.register(FoodLike)
admin.site.register(RestaurantUser)
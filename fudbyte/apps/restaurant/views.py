from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Comment


@login_required()
def restaurant_timeline(request, restaurant_slug):
    print(restaurant_slug)
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    comments = Comment.objects.filter(food__restaurant=restaurant)
    return render(request, 'restaurant/timeline.html', {'restaurant': restaurant, 'comments': comments})

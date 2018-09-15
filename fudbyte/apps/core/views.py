from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from restaurant.models import Restaurant, Food
from fudbyte.utils.slugify_existing import run_sluggy
from fudbyte.utils.models import get_object_or_none


def index(request):
    restaurants = Restaurant.objects.filter(active=True)
    restaurant_filter = request.GET.get('restaurant')
    food_list = Food.objects.filter(active=True)

    if restaurant_filter:
        if restaurant_filter == 'All':
            food_list = Food.objects.filter(active=True)
        else:
            restaurant = get_object_or_none(Restaurant, slug=restaurant_filter)
            if restaurant:
                food_list = Food.objects.filter(restaurant=restaurant)

    page = request.GET.get('page', 1)

    paginator = Paginator(food_list, 10)
    try:
        foods = paginator.page(page)
    except PageNotAnInteger:
        foods = paginator.page(1)
    except EmptyPage:
        foods = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'restaurants': restaurants,
                                          'foods': foods})
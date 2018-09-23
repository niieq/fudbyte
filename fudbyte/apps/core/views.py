from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from restaurant.forms import CommentForm
from restaurant.models import Restaurant, Food, Comment
from fudbyte.utils.models import get_object_or_none
from fudbyte.utils.tasks import assign_kfc_related_images


def index(request):
    restaurants = Restaurant.objects.filter(active=True)
    restaurant_filter = request.GET.get('restaurant')
    food_search = request.GET.get('food')
    food_list = Food.objects.filter(active=True).exclude(image__exact='')

    if restaurant_filter:
        if restaurant_filter == 'All':
            food_list = Food.objects.filter(active=True).exclude(image__exact='')
        else:
            restaurant = get_object_or_none(Restaurant, slug=restaurant_filter)
            if restaurant:
                food_list = Food.objects.filter(restaurant=restaurant).exclude(image__exact='')

    if food_search:
        food_list = Food.objects.filter(name__icontains=food_search).exclude(image__exact='')

    page = request.GET.get('page', 1)

    paginator = Paginator(food_list, 15)
    try:
        foods = paginator.page(page)
    except PageNotAnInteger:
        foods = paginator.page(1)
    except EmptyPage:
        foods = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'restaurants': restaurants,
                                          'foods': foods})


def food_detail(request, food_slug):
    food = get_object_or_404(Food, slug=food_slug)
    comments = Comment.objects.filter(food=food)
    featured = Food.objects.filter(active=True, is_featured=True).exclude(image__exact='')
    return render(request, 'food_detail.html', {'food': food,
                                                'page_title': food.name,
                                                'comments': comments,
                                                'featured': featured})


@login_required()
def post_food_comment(request, food_slug):
    if request.method == 'POST':
        food = get_object_or_404(Food, slug=food_slug)
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.food = food
            comment.save()
            return redirect('/food/{}'.format(food_slug))

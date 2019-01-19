from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Restaurant, Comment, Food, FoodLike, RestaurantUser
from restaurant.forms import CommentForm, FoodForm
from fudbyte.utils.models import get_object_or_none


@login_required()
def restaurant_timeline(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    comments_list = Comment.objects.filter(food__restaurant=restaurant, parent=None)
    page = request.GET.get('page', 1)

    paginator = Paginator(comments_list, 15)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    return render(request, 'restaurant/timeline.html', {'restaurant': restaurant, 'comments': comments})


@login_required()
def post_food_comment(request, restaurant_slug, food_slug):
    if request.method == 'POST':
        food = get_object_or_404(Food, slug=food_slug)
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)

            parent_id = request.POST.get('parent_id')

            if parent_id:
                parent_obj = Comment.objects.get(id=int(parent_id))
                if parent_obj:
                    comment.parent = parent_obj
            comment.user = request.user
            comment.food = food
            comment.save()
            return redirect('/food/{}'.format(food_slug))


@login_required()
def post_food_like(request, restaurant_slug, food_slug):
    food = get_object_or_404(Food, slug=food_slug)
    food_like = get_object_or_none(FoodLike, food=food, user=request.user)
    if food_like:
        food_like.delete()
    else:
        FoodLike.objects.create(food=food, user=request.user)
    return redirect('/')


@login_required()
def foods(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    foods = Food.objects.filter(restaurant=restaurant, active=True)
    can_manage_food = RestaurantUser.can_manage_foods(restaurant, request.user)
    foodform = FoodForm()
    if request.method == 'POST':
        foodform = FoodForm(request.POST, request.FILES)
        if foodform.is_valid():
            if can_manage_food:
                saved_food = foodform.save(commit=False)
                saved_food.restaurant = restaurant
                saved_food.save()
            return redirect('/restaurant/{}/foods'.format(restaurant_slug))
    return render(request, 'restaurant/foods.html', {'foods': foods, 'restaurant': restaurant,
                                                     'can_manage_food': can_manage_food,
                                                     'foodform': foodform})
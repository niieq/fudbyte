from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Comment, Food
from restaurant.forms import CommentForm


@login_required()
def restaurant_timeline(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    comments = Comment.objects.filter(food__restaurant=restaurant, parent=None)
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

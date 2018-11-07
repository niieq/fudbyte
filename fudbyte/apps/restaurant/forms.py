__author__ = 'nii'
from django import forms
from .models import Comment, Food


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'likes', 'food')


class FoodForm(forms.ModelForm):

    class Meta:
        model = Food
        exclude = ('restaurant', 'views', 'is_featured', 'active', 'created_at', 'updated_at')
__author__ = 'nii'
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'likes', 'food')
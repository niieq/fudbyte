__author__ = 'nii'
from django.db import models
from django_extensions.db.fields import ShortUUIDField


class BaseModel(models.Model):

    """
    A Base Model Class
    """

    slug = ShortUUIDField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


def get_object_or_none(model, **kwargs):
    try:
        result = model.objects.get(**kwargs)
    except model.DoesNotExist:
        result = None
    return result
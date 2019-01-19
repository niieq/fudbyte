import requests
from django.db import models
from fudbyte.utils.models import BaseModel
from fudbyte.utils.tasks import get_restaurants_and_food_data


class DataScrap(BaseModel):

    SOURCE_CHOICES = (('jumia_food', 'Jumia Food'),)

    name = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True, choices=SOURCE_CHOICES)

    def __str__(self):
        return self.source

    def save(self, *args, **kwargs):
        get_restaurants_and_food_data.delay()
        super(DataScrap, self).save(*args, **kwargs)
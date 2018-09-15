from django.db import models
from fudbyte.utils.models import BaseModel


class Restaurant(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    restaurant_crawl_link = models.CharField(max_length=255, blank=True, null=True)
    inserted_at = models.DateTimeField()
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'restaurants'

    def __str__(self):
        return self.name


class Food(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    restaurant = models.ForeignKey('Restaurant', models.DO_NOTHING, blank=True, null=True)
    inserted_at = models.DateTimeField()
    image = models.ImageField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True, default=0)
    is_featured = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'foods'

    def __str__(self):
        return self.name

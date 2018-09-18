from django.db import models
from django.utils.text import slugify
from account.models import User
from fudbyte.utils.models import BaseModel


def generate_another_slug(slug, cycle):
    """A function that takes a slug and
    appends a number to the slug

    Examle:
        slug = 'hello-word', cycle = 1
        will return 'hello-word-1'
    """
    if cycle == 1:
        # this means that the loop is running
        # first time and the slug is "fresh"
        # so append a number in the slug
        new_slug = "%s-%s" % (slug, cycle)
    else:
        # the loop is running more than 1 time
        # so the slug isn't fresh as it already
        # has a number appended to it
        # so, replace that number with the
        # current cycle number
        original_slug = "-".join(slug.split("-")[:-1])
        new_slug = "%s-%s" % (original_slug, cycle)

    return new_slug


class Restaurant(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    restaurant_crawl_link = models.CharField(max_length=255, blank=True, null=True)
    inserted_at = models.DateTimeField()
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'restaurants'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:

            slug = slugify(self.name)

            cycle = 1 # the current loop cycle

            while True:
                # this loop will run until the slug is unique
                try:
                    Restaurant.objects.get(slug=slug)
                except Restaurant.DoesNotExist:
                    self.slug = slug
                    self.save()
                    break
                else:
                    slug = generate_another_slug(slug, cycle)

                cycle += 1 # update cycle number
        super(Restaurant, self).save(*args, **kwargs)


class Food(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    restaurant = models.ForeignKey('Restaurant', models.DO_NOTHING, blank=True, null=True)
    inserted_at = models.DateTimeField()
    image = models.ImageField(blank=True, null=True, upload_to='food_images')
    likes = models.IntegerField(blank=True, null=True, default=0)
    is_featured = models.BooleanField()
    slug = models.CharField(max_length=255, blank=True, null=True, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'foods'

    def __str__(self):
        return self.name

    def comments(self):
        return Comment.objects.filter(food=self)

    def save(self, *args, **kwargs):
        if not self.slug:

            slug = slugify(self.name)

            cycle = 1 # the current loop cycle

            while True:
                # this loop will run until the slug is unique
                try:
                    Food.objects.get(slug=slug)
                except Food.DoesNotExist:
                    self.slug = slug
                    self.save()
                    break
                else:
                    slug = generate_another_slug(slug, cycle)

                cycle += 1 # update cycle number
        super(Food, self).save(*args, **kwargs)


class Comment(BaseModel):
    food = models.ForeignKey(Food, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    message = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='comment_images')
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.message
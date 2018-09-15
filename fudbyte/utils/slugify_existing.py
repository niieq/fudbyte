__author__ = 'nii'
from django.utils.text import slugify

from restaurant.models import Restaurant, Food


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

# The for loop to create new slugs and update db records

def run_sluggy():
    for obj in Food.objects.all():
        if not obj.slug: # only create slug if empty

            slug = slugify(obj.name)[:20]

            cycle = 1 # the current loop cycle

            while True:
                # this loop will run until the slug is unique
                try:
                    model = Food.objects.get(slug=slug)
                except Food.DoesNotExist:
                    obj.slug = slug
                    obj.save()
                    break
                else:
                    slug = generate_another_slug(slug, cycle)

                cycle += 1 # update cycle number


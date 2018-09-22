__author__ = 'nii'
import imghdr # Used to validate images
import urllib.request # Used to download images
from django.core.files.base import ContentFile
from io import StringIO, BytesIO # Used to imitate reading from byte file
from PIL import Image # Holds downloaded image and verifies it
import copy # Copies instances of Image
import requests
from bs4 import BeautifulSoup
from fudbyte.celery import app
from restaurant.models import Restaurant, Food
from fudbyte.utils.models import get_object_or_none

@app.task
def get_restaurants_and_food_data():
    r = requests.get('https://api.food.jumia.com.gh/api/v5/vendors', headers={"X-FP-API-KEY": "HTML5"})
    restaurants = r.json()["data"]["items"]

    for restaurant in restaurants:
        if restaurant['name'] == 'Hellofood Test Restaurant 2' or restaurant['name'] == 'Hellofood Test Restaurant 2':
            print('test restaurants avoid')
        else:
            existing_restaurant = get_object_or_none(Restaurant, name=restaurant['name'])
            if not existing_restaurant:
                rest_obj = Restaurant()
                rest_obj.name = restaurant['name']
                rest_obj.restaurant_crawl_link = restaurant['web_path']
                rest_obj.description = restaurant['description']
                rest_obj.city = restaurant['city']['name']
                rest_obj.address = '{} \n {}'.format(restaurant['address'], restaurant['address_line2'] if restaurant['address_line2'] else '')
                rest_obj.latitude = restaurant['latitude']
                rest_obj.longitude = restaurant['longitude']
                logo_path = restaurant['logo'].split('%s/')
                if len(logo_path) == 3:
                    img = download_image(logo_path[2])
                    try:
                        filename = '{}.{}'.format(restaurant['name'].replace(' ', '_'), img.format)
                        rest_obj.logo = filename
                        tempfile = img
                        tempfile_io = BytesIO() # Will make a file-like object in memory that you can then save
                        tempfile.save(tempfile_io, format=img.format)
                        rest_obj.logo.save(filename, ContentFile(tempfile_io.getvalue()), save=False) # Set save=False otherwise you will have a looping save method
                    except:
                        print("Error trying to save model: saving image failed: ")
                        pass
                if restaurant['cms_content']['vendor_wide_logo']:
                    try:
                        img = download_image(restaurant['cms_content']['vendor_wide_logo'])
                        filename = '{}_cover.{}'.format(restaurant['name'].replace(' ', '_'), img.format)
                        rest_obj.cover_photo = filename
                        tempfile = img
                        tempfile_io = BytesIO() # Will make a file-like object in memory that you can then save
                        tempfile.save(tempfile_io, format=img.format)
                        rest_obj.cover_photo.save(filename, ContentFile(tempfile_io.getvalue()), save=False) # Set save=False otherwise you will have a looping save method
                    except:
                        print("Error trying to save model: saving image failed: ")
                        pass
                rest_obj.save()
            food_path = requests.get(restaurant['web_path'])
            soup = BeautifulSoup(food_path.text, 'html.parser')
            food_items = soup.find_all('article', class_='product-variation')
            food_name_parent = None
            for food_item in food_items:
                the_food_name = None
                food_name = food_item.find('span', class_='mrs')
                right_text_food = food_item.find('div', class_='has-text-right')

                if food_name and right_text_food:
                    right_text_food_select = right_text_food.find('span', class_='has-ellipsis')
                    food_name_parent = food_name.get_text()
                    the_food_name = '{} {}'.format(food_name.get_text(), right_text_food_select.get_text())
                elif right_text_food and not food_name:
                    right_text_food_select = right_text_food.find('span', class_='has-ellipsis')
                    the_food_name = '{} {}'.format(food_name_parent, right_text_food_select.get_text())
                elif food_name:
                    food_name = food_name.get_text()
                    food_name_parent = food_name
                    the_food_name = food_name

                food_description = food_item.find('p', class_='dsc').get_text() if food_item.find('p', class_='dsc') else ''
                food_price = food_item.find('span', class_='mlxs').get_text()

                existing_food = get_object_or_none(Food, name=the_food_name)
                if not existing_food:
                    food_obj = Food()
                    food_obj.name = the_food_name.strip()
                    food_obj.description = food_description.strip()
                    food_obj.price = food_price
                    food_obj.restaurant = rest_obj if not existing_restaurant else existing_restaurant
                    food_obj.save()


def download_image(url):
    """Downloads an image and makes sure it's verified.

    Returns a PIL Image if the image is valid, otherwise raises an exception.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'} # More likely to get a response if server thinks you're a browser
    r = urllib.request.Request(url, headers=headers)
    request = urllib.request.urlopen(url, timeout=10)
    image_data = BytesIO(request.read()) # StringIO imitates a file, needed for verification step
    img = Image.open(image_data) # Creates an instance of PIL Image class - PIL does the verification of file
    img_copy = copy.copy(img) # Verify the copied image, not original - verification requires you to open the image again after verification, but since we don't have the file saved yet we won't be able to. This is because once we read() urllib2.urlopen we can't access the response again without remaking the request (i.e. downloading the image again). Rather than do that, we duplicate the PIL Image in memory.
    if valid_img(img_copy, img.format):
        return img
    else:
        # Maybe this is not the best error handling...you might want to just provide a path to a generic image instead
        raise Exception('An invalid image was detected when attempting to save a Product!')


def valid_img(img, img_format):
    """Verifies that an instance of a PIL Image Class is actually an image and returns either True or False."""
    type = img_format
    if type in ('GIF', 'JPEG', 'JPG', 'PNG'):
        try:
            img.verify()
            return True
        except:
            return False
    else: return False


@app.task
def assign_kfc_related_images():
    foods = Food.objects.filter(restaurant__name='KFC (Tema Community 11)')
    for food in foods:
        other_foods = Food.objects.filter(name=food.name).exclude(restaurant__name='KFC (Tema Community 11)')
        for other_food in other_foods:
            new_image = ContentFile(food.image.read())
            new_image.name = food.file.name
            other_food.image = new_image
            other_food.save()



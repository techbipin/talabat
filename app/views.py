from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.conf import settings


def save_image_from_url(url):
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen(url).read())
    img_temp.flush()
    return ContentFile(img_temp.read())


def save_products_from_json():
    import json
    from .models import Category, Product

    with open(settings.BASE_DIR/'data.json', 'r') as f:
        data = json.load(f)

    for category_name, category_data in data.items():
        try:
            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                category = Category.objects.create(name=category_name)

            for item_data in category_data['items']:
                product = Product.objects.create(
                    name=item_data['item_name'],
                    description=item_data['item_desc'],
                    price=item_data['item_price'],
                    category=category
                )
                if item_data['image_url']:
                    product.image.save(f"{category_name}_{product.pk}.jpg", save_image_from_url(item_data['image_url']), save=True)
        except Exception as ep:
            print(f"{ep=}")

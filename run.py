import json
from pathlib import Path
import time
import django
from django.conf import settings
from modules.common.product import Product
from modules.common.download_chromedriver import check_equality_version


BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)
INSTALLED_APPS = ['visky']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data/db.sqlite3',
    }
}
SETTINGS = dict((key, val) for key, val in locals().items() if key.isupper())

if not settings.configured:
     settings.configure(**SETTINGS)

django.setup()


from visky.models import Alcohol
from main import get_list_of_alcohol_in_rozetka


def load_all_alcohols(filename: str):
    print(filename)
    with open(BASE_DIR / filename, 'r') as file:
        try:
            read_alcohols = json.load(file)
            for alcohol in read_alcohols:
                yield alcohol
        except json.decoder.JSONDecodeError:
            pass


def write_to_db(alcohol: Product):
    # del alcohol['id']
    # alcohol['characteristic'] = json.dumps(alcohol['characteristic'], indent=8)
    # Alcohol.objects.update_or_create(name=alcohol['name'],
    #                        price=alcohol['price'],
    #                        image=alcohol['img'],
    #                        product_link=alcohol['link'],
    #                        product_code=alcohol['code'],
    #                        description=alcohol['characteristic'] if alcohol['characteristic'] else [(None, None),])

    p, created = Alcohol.objects.get_or_create(product_code=alcohol['code'],
                                  defaults={
                                      'name': alcohol['name'],
                                      'prices': [{
                                          time.strftime("%Y/%m/%d", time.localtime()): alcohol['price']},
                                      ],
                                      'image': alcohol['img'],
                                      'product_link': alcohol['link'],
                                      'description': alcohol['characteristic'],


                                  })
    print(p)
    if not created:
        p.prices.insert(0, {time.strftime("%Y/%m/%d", time.localtime()): alcohol['price']})
        p.save()


if __name__ == '__main__':
    check_equality_version()
    # alcohol_atb = get_list_of_alcohols()
    # for alcohol in alcohol_atb:
    #     write_to_db(alcohol.to_dict())
    alcohol_rozetka = get_list_of_alcohol_in_rozetka()
    for alcohol in alcohol_rozetka:
        write_to_db(alcohol.to_dict())

    # print(BASE_DIR.parent)
    # filenames = glob.glob(str(BASE_DIR) + r'/alcohol*.json')
    # print(filenames)
    # for name in filenames:
    #     print(name)
    #     for el in load_all_alcohols(name):
    #         write_to_db(el)


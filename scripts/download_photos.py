import subprocess
from products.models import Product
from visky.models import Alcohol
from django.conf import settings


def run():
    for link, *_ in Product.objects.values_list('image'):
    
        subprocess.run(["wget",
                        "-b", f"{link}",
                        "-P", settings.STATICFILES_DIRS[0] + "/images/economy"])

    for link, *_ in Alcohol.objects.values_list('image'):
    
        subprocess.run(["wget",
                        "-b", f"{link}",
                        "-P", settings.STATICFILES_DIRS[0] + "/images/alcohol"])




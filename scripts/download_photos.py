import subprocess
from products.models import Product
from visky.models import Alcohol
from alcohol.settings import BASE_DIR

def run():
    for product in Product.objects.all():
        subprocess.run(["wget",
                        "-b", f"{product.image}", 
                        "-P", BASE_DIR / "static/images/economy"])

    #for alcohol in Alcohol.objects.values_list('image'):
    #    link, *_ = alcohol
    #    subprocess.run(["wget",
    #                     "-b", f"{link}",
    #                     "-P", BASE_DIR / "static/images/visky"])

    return 1

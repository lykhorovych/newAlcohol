import subprocess
from products.models import Product


def run():
    for product in Product.objects.all():
        print(["wget", "-b", f"{product.image}", "-P", r"./static/images"])
        subprocess.run(["wget", "-b", f"{product.image}", "-P", r"./static/images"])



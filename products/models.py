from django.db import models
import time
# Create your models here.
#class Category(models.Model):
#    name = models.CharField()
#
#    def __str__(self) -> str:
#        return f"{self.name}"


class Product(models.Model):
    rating = models.SmallIntegerField(validators=[])
    discount = models.SmallIntegerField(validators=[])
    name = models.CharField(blank=True, null=True, max_length=128, help_text="product description")
    image = models.URLField(blank=True, null=True, help_text="link to image")
    link = models.URLField(blank=True, null=True, help_text="product link")
    price_top = models.FloatField(help_text="price without discount")
    price_bottom = models.FloatField(help_text="price with discount")
    price_statistic = models.JSONField(blank=True, null=True)
    #product_id = models.IntegerField()
    in_economy = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_ends = models.BooleanField(default=False)
    #category = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return f"{self.name}"
    
    def get_or_create(self, **kwargs):
        product, is_not_exists = Product.objects.get_or_create()
        if not is_not_exists:
            product.save()
        return product
    
    #def update_or_create(self, defaults):
    #    product, is_exists = Product.objects.update_or_create(name = desc, 
    #                                                                      defaults={
    #                                                                           'is_available': available,
    #                                                                           'is_ends': ends,
    #                                                                           },
    #                                                                      create_defaults=credentials)
    #    if not is_exists:
    #        product.price_statistic.append((time.strftime("%Y/%m/%d", time.localtime()), price_top))
    #        product.save()
    #    return product

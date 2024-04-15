
from django.db import models

# Create your models here.


# class PricesModel(models.Model):
#     product_id = models.OneToOneField('Alcohol', on_delete=models.CASCADE, primary_key=True, related_name='alcohol_price')
#     prices = models.JSONField(default=dict, blank=True, null=True)
#
#     def __str__(self):
#         return self.prices
#
#     def create(self):
#         pass
#
#     class Meta:
#         verbose_name = 'price'
#         verbose_name_plural = 'prices'
#

class Alcohol(models.Model):
    name = models.CharField(max_length=256)
    prices = models.JSONField(blank=True, null=True)
    image = models.CharField(max_length=128)
    product_link = models.CharField(max_length=256)
    product_code = models.IntegerField(db_index=True)
    description = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.prices}"

    class Meta:
        verbose_name = "alcohol"
        verbose_name_plural = "alcohols"

    # @classmethod
    # def create(cls, **kwargs):
    #     code = kwargs["product_code"]
    #     price = kwargs['price']
    #     date = time.strftime("%Y/%m/%d", time.localtime())
    #     try:
    #         print(code, price)
    #         obj = cls.objects.filter(product_code=code).first()
    #         price = {date: price}
    #         print(obj)
    #         obj.update(kwargs).save()
    #     except cls.DoesNotExist:
    #         # data = json.dumps([{date: price}, ])
    #         obj = cls.objects.create(**kwargs)
    #     return obj
    #     cls.objects.get_or_create(product_code=code, )




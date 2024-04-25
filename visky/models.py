from django.db import models


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


class Tag(models.Model):

    name = models.SlugField(
        max_length=32,
        db_index=True,
        unique=True,
        help_text='Tag name'
    )

    def __str__(self):
        return self.name





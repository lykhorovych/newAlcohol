from django.contrib import admin

from visky.models import Alcohol


# Register your models here.
class AlcoholAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_code')
    fields = ('name', 'product_code')


admin.site.register(Alcohol, AlcoholAdmin)

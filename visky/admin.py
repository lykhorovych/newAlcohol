from django.contrib import admin

from visky.models import Alcohol, Tag


# Register your models here.
class AlcoholAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_code')
    fields = ('name', 'product_code')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    fields = ('name', )


admin.site.register(Alcohol, AlcoholAdmin)
admin.site.register(Tag, TagAdmin)

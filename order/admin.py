from django.contrib import admin
from django.utils.html import format_html

from .models import Order
from shop.models import Cake, Category, CustomUser


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(CustomUser)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['phone_number']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', "phonenumber", "delivery_date", "delivery_time"]
    ordering = ['-delivery_date', ]


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    def image_tag(self, cake):
        return format_html(
            '<img style="max-height:{height}" src="{url}"/>',
            url=cake.image.url,
            height='100px',
        )

    image_tag.short_description = 'Photo'
    list_display = ['name', 'description', 'price', 'category', 'image_tag']
    ordering = ['name']

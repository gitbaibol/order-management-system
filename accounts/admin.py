from django.contrib import admin
from django.utils.html import format_html
from . import models

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'date_created', 'profile_picture']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['date_created']
    
    def profile_picture(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_pic.url)
        return "—"
    profile_picture.short_description = 'Фото'

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']
    list_filter = ['price']

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'status', 'date_created']
    list_filter = ['status', 'date_created']
    search_fields = ['product__name', 'customer__name', 'note']
    raw_id_fields = ['customer']
    list_per_page = 20
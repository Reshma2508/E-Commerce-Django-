from django.contrib import admin

# Register your models here.
from .models import Product

class adclass(admin.ModelAdmin):
        list_display = ["title","price","discount_price","category","description","image"]

admin.site.register(Product,adclass)
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity'] 

@admin.register(OrderPlaced)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','order_date','status']
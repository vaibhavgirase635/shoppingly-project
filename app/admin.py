from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.
admin.site.register(Customer)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','specifications','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity'] 

@admin.register(OrderPlaced)
class OrderplacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','customer_info','product','product_info','quantity','order_date','status']

    def customer_info(self,obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    def product_info(self,obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(ReviewRating)
class ProductReviewModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','subject','review','rating', 'ip', 'status', 'created_at', 'updated_at'] 
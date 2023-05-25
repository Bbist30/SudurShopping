from django.contrib import admin
from .models import (
    Customer,
    Product,
    Cart,
    Orderplaced
)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(Orderplaced)
class OrderplacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_username', 'customer', 'product', 'quantity', 'user', 'status']

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'User'

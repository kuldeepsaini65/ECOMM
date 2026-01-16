from django.contrib import admin
from .models import Products, Cart, Order, OrderItemHistory
from django.contrib.admin.decorators import register


@register(Products)
class ProductsAdminList(admin.ModelAdmin):
    list_display = ['name','price','description']

@register(Cart)
class CartAdminList(admin.ModelAdmin):
    list_display = ['user','item','quantity','created_at']

@register(Order)
class OrderAdminList(admin.ModelAdmin):
    list_display = ['user','stripe_session_id','total_amount','status','created_at']

@register(OrderItemHistory)
class OrderAdminList(admin.ModelAdmin):
    list_display = ['order','product','quantity','price']

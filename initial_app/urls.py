from django.urls import path
from .views import *

app_name = 'initial'

urlpatterns = [
    path('', home, name='home'),
    path('add-to-cart/', add_cart, name='add_cart'),
    path('remove-cart-item/<int:id>', cart_delete, name='cart_delete'),
    path("checkout/", create_checkout_session, name="checkout"),
    path("stripe/webhook/", stripe_webhook, name="stripe-webhook"),
    
    path("order/success/", order_success, name="striorder_successe"),
    path("order/cancel/", order_cancel, name="order_cancel"),


]

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import stripe 
from django.conf import settings
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    context = {}
    context['data'] = Products.objects.all()
    context['cart_items'] = Cart.objects.filter(user=request.user)
    return render(request, 'index.html', context = context)


def add_cart(request):
    if request.method != "POST":
        messages.error(request, 'Request method is not Valid..')
        return redirect('initial:home')

    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')

    try:
        quantity = int(quantity)
        product = Products.objects.get(id=product_id)

        Cart.objects.create(user=request.user,item=product,quantity=quantity)
        messages.success(request, "Item added to cart successfully")

    except Exception as e:
        messages.error(request, f"Failed to add item: {e}")

    return redirect('initial:home')


def cart_delete(request, id):
    cart_item = Cart.objects.get(id=id)
    if cart_item.user == request.user:
        cart_item.delete()
        messages.success(request, f'{cart_item.item.name} has been removed from Cart.')
    else:
        messages.error(request, f'Request Rejected by System.')

    return redirect('initial:home')





from decimal import Decimal

@login_required
def create_checkout_session(request):
    cart_items = Cart.objects.select_related("item").filter(user=request.user)

    line_items = []
    total_amount_inr = Decimal("0.00")

    for cart in cart_items:
        price_inr = cart.item.price 
        total_amount_inr += price_inr * cart.quantity

        line_items.append({
            "price_data": {
                "currency": "inr",
                "product_data": {
                    "name": cart.item.name,
                },
                "unit_amount": int(price_inr * 100),
            },
            "quantity": cart.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="http://127.0.0.1:8000/order/success/",
        cancel_url="http://127.0.0.1:8000/order/cancel/",
    )

    order = Order.objects.create(
        user=request.user,
        stripe_session_id=session.id,
        total_amount=total_amount_inr,
        status="PENDING",
    )

    for cart in cart_items:
        OrderItemHistory.objects.create(
            order=order,
            product=cart.item,
            quantity=cart.quantity,
            price=cart.item.price,
        )

    return redirect(session.url, code=303)




@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    print(payload)
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(payload,sig_header,settings.STRIPE_WEBHOOK_SECRET)

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    except ValueError:
        return HttpResponse(status=400)


    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        try:
            order = Order.objects.get(stripe_session_id=session["id"])
            order.status = "PAID"
            order.save()

            Cart.objects.filter(user=order.user).delete()

        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)



def order_success(request):
    return HttpResponse('Payment Success')

def order_cancel(request):
    return HttpResponse('Payment Canceld due to an error')
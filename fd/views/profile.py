from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import stripe
import djstripe
#from pinax.stripe.actions import customers, subscriptions


@csrf_exempt
def get_user_profile(request):
    if request.method == "POST":
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
        token = request.POST['stripeToken']
        email = request.POST['stripeEmail']
        
        try:
            charge = stripe.Customer.create(
                email=email,
                source=token,
                plan='fedry'
            )
            messages.info(request, "Payment is successful")
        except stripe.error.CardError as e:
            # The card has been declined
            print(e.message)
            pass
    
#    user = request.user
#    customer = customers.get_customer_for_user(request.user)
#    sub = subscriptions.retrieve(customer, '')
#    sub = subscriptions.has_active_subscription(customer)

    sub = djstripe.utils.subscriber_has_active_subscription(request.user)
    return render(request, 'fd/profile.html', {"user": request.user, "sub": sub})

@csrf_exempt
def subscribe(request):
    if request.method == "POST":
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
        token = request.POST['stripeToken']
        email = request.POST['stripeEmail']
        
        try:
            charge = stripe.Customer.create(
                email=email,
                source=token,
                plan='fedry'
            )
            messages.info(request, "Payment is successful")
        except stripe.error.CardError as e:
            # The card has been declined
            print(e.message)
            pass
        
    return render(request, 'fd/subscribe.html', {"user": request.user})

from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from fd.forms import SignUpForm
import stripe
import djstripe

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
                plan='Fedry'
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
                plan='Fedry'
            )
            messages.info(request, "Payment is successful")
        except stripe.error.CardError as e:
            # The card has been declined
            print(e.message)
            pass
        
    return render(request, 'fd/subscribe.html', {"user": request.user})

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'fd/signup.html', {'form': form})

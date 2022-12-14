from django.shortcuts import render, redirect

from django.contrib import messages

from .forms import PaymentForm
from .paystack import Paystack

from django.conf import settings

import secrets


# Create your views here.
def initiate_payment(request):
    payment_form = PaymentForm()

    if request.method == "POST":
        payment_form = PaymentForm(request.POST)

        if payment_form.is_valid():
            cd = payment_form.cleaned_data

            # Create session values from the form data and generate ref value
            ref = secrets.token_urlsafe(50)

            request.session["amount"] = cd["amount"]
            request.session["email"] = cd["email"]
            request.session["ref"] = ref

            ctx = {
                "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY,
                "ref": ref,
                "amount": cd["amount"],
                "email": cd["email"],
            }

            return render(request, "payments/make_payment.html", ctx)

    return render(request, "payments/initiate_payment.html", {"payment_form": payment_form})


def verify_payment(request, ref):
    paystack = Paystack()
    verified = False

    # Get the values from the session
    ref = request.session["ref"]
    amount = request.session["amount"]

    status, result = paystack.verify_payment(ref, amount)

    if status:
        if result["amount"] / 100 == amount:
            verified = True

    if verified:
        messages.success(request, 'Your payment has been verified')
    else:
        messages.error(request, 'Your payment could not be verified')

    return redirect("initiate_payment")

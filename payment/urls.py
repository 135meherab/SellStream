
# urls.py
from django.urls import path
from .views import InitiatePaymentView, payment_success, payment_fail, payment_cancel

urlpatterns = [
    path('initiate-payment/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payment-success/', payment_success, name='payment-success'),
    path('payment-fail/', payment_fail, name='payment-fail'),
    path('payment-cancel/', payment_cancel, name='payment-cancel'),
]

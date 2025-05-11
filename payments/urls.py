from django.urls import path
from . import views

app_name = 'payments'  # এই লাইন যোগ করুন

urlpatterns = [
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
    path('process/', views.process_payment, name='process_payment'),
]
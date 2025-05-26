from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/', views.initiate_payment, name='initiate_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
]
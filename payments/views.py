import uuid
import requests
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Payment
from core.models import Order

def initiate_payment(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount') or 100)
        order_id = request.POST.get('order_id')

        order = None
        if order_id:
            try:
                order = Order.objects.get(id=int(order_id))
            except (Order.DoesNotExist, ValueError):
                order = None

        transaction_id = str(uuid.uuid4())

        payment = Payment.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order=order,
            amount=amount,
            transaction_id=transaction_id,
            payment_status='Pending',
            currency='BDT'
        )

        payload = {
            'store_id': settings.SSL_COMMERZ['store_id'],
            'store_passwd': settings.SSL_COMMERZ['store_pass'],
            'total_amount': amount,
            'currency': 'BDT',
            'tran_id': transaction_id,
            'success_url': request.build_absolute_uri('/payments/success/'),
            'fail_url': request.build_absolute_uri('/payments/failed/'),
            'cancel_url': request.build_absolute_uri('/payments/cancel/'),
            'cus_name': request.POST.get('cus_name', 'Customer'),
            'cus_email': request.POST.get('cus_email', 'customer@example.com'),
            'cus_phone': request.POST.get('cus_phone', '01700000000'),
            'cus_add1': request.POST.get('cus_add1', 'Dhaka'),
            'cus_city': 'Dhaka',
            'cus_country': 'Bangladesh',
            'shipping_method': 'NO',
            'product_name': 'Ecommerce Order',
            'product_category': 'General',
            'product_profile': 'general'
        }

        try:
            response = requests.post(settings.SSL_COMMERZ['init_url'], data=payload)
            data = response.json()

            if data.get('status') == 'SUCCESS':
                request.session['transaction_id'] = transaction_id
                return redirect(data['GatewayPageURL'])
            else:
                payment.payment_status = 'Failed'
                payment.save()
                return render(request, 'payments/payment_failed.html', {
                    'error': data.get('failedreason', 'Unknown error')
                })
        except Exception as e:
            payment.payment_status = 'Failed'
            payment.save()
            return render(request, 'payments/payment_failed.html', {
                'error': str(e)
            })

    return render(request, 'core/checkout.html')


@csrf_exempt
def payment_success(request):
    transaction_id = request.GET.get('tran_id') or request.session.get('transaction_id')
    if transaction_id:
        payment = Payment.objects.filter(transaction_id=transaction_id).first()
        if payment:
            payment.payment_status = 'Completed'
            payment.save()
    return render(request, 'payments/payment_success.html')


@csrf_exempt
def payment_failed(request):
    transaction_id = request.GET.get('tran_id') or request.session.get('transaction_id')
    if transaction_id:
        payment = Payment.objects.filter(transaction_id=transaction_id).first()
        if payment:
            payment.payment_status = 'Failed'
            payment.save()
    return render(request, 'payments/payment_failed.html')


@csrf_exempt
def payment_cancel(request):
    transaction_id = request.GET.get('tran_id') or request.session.get('transaction_id')
    if transaction_id:
        payment = Payment.objects.filter(transaction_id=transaction_id).first()
        if payment:
            payment.payment_status = 'Cancelled'
            payment.save()
    return render(request, 'payments/payment_cancel.html')

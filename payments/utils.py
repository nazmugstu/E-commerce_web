import requests
from django.conf import settings

def initiate_payment(order):
    data = {
        'store_id': settings.SSL_STORE_ID,
        'store_passwd': settings.SSL_STORE_PASSWORD,
        'total_amount': order.total_price,
        'currency': 'BDT',
        'tran_id': str(order.transaction_id),
        'success_url': 'http://yourdomain.com/payments/success/',
        'fail_url': 'http://yourdomain.com/payments/fail/',
        'cancel_url': 'http://yourdomain.com/payments/cancel/',
        'cus_name': order.user.username,
        'cus_email': order.user.email,
        'cus_phone': order.user.phone,
        'cus_add1': order.user.address,
        'shipping_method': 'NO',
        'product_name': 'Ecommerce Order',
        'product_category': 'Ecommerce',
        'product_profile': 'general',
    }

    response = requests.post(settings.SSL_API_URL, data=data)
    res_data = response.json()

    if res_data.get('status') == 'SUCCESS':
        return res_data['GatewayPageURL']
    else:
        return None

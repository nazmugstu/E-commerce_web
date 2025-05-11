from sslcommerz_lib import SSLCOMMERZ

def initiate_payment(amount, user):
    settings = {'store_id': 'your_store_id', 'store_pass': 'your_store_password', 'issandbox': True}
    sslcommerz = SSLCOMMERZ(settings)
    return sslcommerz
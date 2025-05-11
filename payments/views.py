from django.shortcuts import render

def process_payment(request):
    # পেমেন্ট প্রসেসিং লজিক যোগ করুন (যেমন SSLCommerz)
    return render(request, 'payments/process_payment.html')

def payment_success(request):
    # পেমেন্ট সফল হলে লজিক
    return render(request, 'payments/payment_success.html')

def payment_failed(request):
    # পেমেন্ট ব্যর্থ হলে লজিক
    return render(request, 'payments/payment_failed.html')
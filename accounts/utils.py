from django.core.mail import send_mail

def send_verification_email(user, verification_url):
    send_mail(
        'Verify Your Email',
        f'Click the link to verify: {verification_url}',
        'from@example.com',
        [user.email],
    )
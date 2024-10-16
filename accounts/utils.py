from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes

def send_activation_email(user, request):
    # Generate JWT for email activation
    try:
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)  # Get access token

        # Prepare the email
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        activation_link = f"http://{current_site.domain}/account/activate/{token}/"

        message = f"Hi {user.email},\nClick the link below to activate your account:\n{activation_link}"

        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()
    except Exception as e:
        # Add error logging for troubleshooting
        print(f"Error sending activation email: {e}")
        raise e
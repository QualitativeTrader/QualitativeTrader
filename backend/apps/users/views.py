from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Account
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .tokens import account_activation_token

@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = json.loads(request.body)['email']

        if Account.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email is already registered'}, status=400)
        
        user = Account.objects.create(email=email)
        user.is_auth = False
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        activation_link = request.build_absolute_uri(
            reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
        )

        subject = 'Activate your account'
        message = render_to_string('auth_email.html', {'url': str(activation_link)})


        email = EmailMultiAlternatives(
            subject=subject, 
            body=None,
            from_email=None,
            to=[user.email]
        )
        email.attach_alternative(message, "text/html")
        email.send()

        return JsonResponse({'success': True, 'message': 'Activation email sent'}, status=201)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None


    if user is not None and account_activation_token.check_token(user, token):
        if user.is_auth:
            return JsonResponse({'success': False, 'message': 'User already verified'}, status=400)
        else:
            user.is_auth = True
            user.auth_password = uuid.uuid4().hex
            user.save()


            deactivation_link = request.build_absolute_uri(
                reverse('deactivate', kwargs={'uidb64': uidb64, 'auth_password': user.auth_password})
            )
            message = render_to_string('success_email.html', {'url': str(deactivation_link)})

            email = EmailMultiAlternatives(
            subject="Account Verification Successful!", 
            body=None,
            from_email=None,
            to=[user.email]
            )
            email.attach_alternative(message, "text/html")
            email.send()
            
            return JsonResponse({'success': True, 'message': 'Account activated successfully!'}, status=200)

    return JsonResponse({'success': False, 'message': 'Activation failed'}, status=400)

@csrf_exempt
def deactivate(request, uidb64, auth_password):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None


    if user is not None and user.auth_password == auth_password:
        user.delete()

        return JsonResponse({'success': True, 'message': 'Account deleted successfully!'}, status=200)

    return JsonResponse({'success': False, 'message': 'Deletion failed'}, status=400)
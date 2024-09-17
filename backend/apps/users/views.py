from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .tokens import account_activation_token

@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = json.loads(request.body)['email']

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email is already registered'}, status=400)
        
        user = User.objects.create(email=email)
        user.set_unusable_password()
        user.is_active = False
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        activation_link = request.build_absolute_uri(
            reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
        )

        subject = 'Activate your account'
        message = f'Hello, please click the link to activate your account: {activation_link}'
        send_mail(subject, message, None, [user.email])

        return JsonResponse({'success': True, 'message': 'Activation email sent'}, status=201)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None


    if user is not None and account_activation_token.check_token(user, token):
        if user.is_active:
            return JsonResponse({'success': False, 'message': 'User already verified'}, status=400)
        else:
            user.is_active = True
            user.save()
            return JsonResponse({'success': True, 'message': 'Account activated successfully!'}, status=200)

    return JsonResponse({'success': False, 'message': 'Activation failed'}, status=400)
    

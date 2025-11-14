from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django_ratelimit.decorators import ratelimit

User = get_user_model()


@ratelimit(key='ip', rate='5/m', method='POST')
def forgot_password_view(request):
    """Send password reset email with token link and rate limiting."""
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            messages.error(request, 'Too many password reset attempts. Please try again in a few minutes.')
            return render(request, 'users/forgot_password.html')
        
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
            # Generate token and uidb64
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build reset link
            reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
            
            # Send email
            subject = 'Password Reset Request - Library Management'
            message = f"""
Hello {user.username},

You requested a password reset. Click the link below to reset your password:

{reset_link}

This link is valid for 24 hours.

If you did not request this, please ignore this email.

Best regards,
Library Management System
"""
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            messages.success(request, 'Password reset link sent to your email.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
        except Exception as e:
            messages.error(request, f'Error sending email: {str(e)}')
    
    return render(request, 'forgot_password.html')


def reset_password_view(request, uidb64, token):
    """Validate token and allow user to set new password."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 and password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, 'Password reset successful. Please login with your new password.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        
        return render(request, 'reset_password.html', {'validlink': True, 'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'Password reset link is invalid or has expired.')
        return render(request, 'reset_password.html', {'validlink': False})

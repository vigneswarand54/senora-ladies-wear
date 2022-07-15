from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator    
from django.contrib.sites.shortcuts import get_current_site
from django.forms import ValidationError
from .verify import check,send
from django.shortcuts import redirect, render
from .forms import UserCreationForm, registrationform
from accounts.models import accounts
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def otp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone = request.session['phonenumber']
            if check(phone,code):
                user = accounts.objects.get(phone = phone)
                user.is_active = True
                user.save()
                return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register_otp.html',{'form':form})

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if accounts.objects.filter(email=email).exists():
            user = accounts.objects.get(email__exact=email)
            
            # Forgot password
            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            print(email)
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            print('hello')
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            print('fdgd')
            send_email.send()

            messages.success(request, ' Password reset link has been sent to your email address')
            return redirect('login')


        else:
            messages.error(request, 'Account does not exsist')
            return redirect('forgotpassword')


    return render(request, 'accounts/forgot_password.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = accounts._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, accounts.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Set Your New Password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('login')

def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = accounts.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password Reset Successfully")
            return redirect('login')
        else:
            messages.error(request, 'Password Does Not Match')
            return redirect('resetpassword')
    else:
        return render(request, 'accounts/reset_password.html')

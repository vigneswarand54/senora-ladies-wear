from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('OTP-verification/',views.otp, name='otp'), 
    path('forgotpassword/', views.forgotPassword, name= 'forgotpassword'),
    path('validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/',views.resetpassword, name= 'resetpassword')
]
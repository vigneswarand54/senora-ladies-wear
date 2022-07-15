from django import forms
from accounts.models import accounts
from django.contrib import messages

#registration form

class registrationform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))
    
    class Meta:
        model=accounts
        fields = ['first_name','last_name','email','phone','password','confirm_password' ]
        
    def clean(self):
        cleaned_data = super(registrationform,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
            )
        
    def __init__(self, *args, **kwargs):

        super(registrationform, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    
class UserCreationForm(forms.Form,):
    code = forms.CharField(max_length=6, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter OTP',
        'class': 'form-control-lg',
    }))
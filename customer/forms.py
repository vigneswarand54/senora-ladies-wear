from django import forms
from customer.models import Delivery_address
from accounts.models import accounts


class addressform(forms.Form):
    class meta:
        model = Delivery_address
        fields = ['firstname','lastname','addressfield_1','addressfield_2','city','state','country','post_code','phonenumber','email']

class updateuserform(forms.ModelForm):
    class Meta:
        model = accounts
        fields = ['first_name', 'last_name','email','phone']
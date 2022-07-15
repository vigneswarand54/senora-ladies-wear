from pyexpat import model
from django import forms
from .models import reviewrating


class reviewform(forms.ModelForm):
    class Meta:
        model = reviewrating
        fields =['subject','review','rating']
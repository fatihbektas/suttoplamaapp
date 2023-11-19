from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *


class OrderAddressForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'note']


class OrderAssignForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['user']

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {'user': _("Servis Adı")}

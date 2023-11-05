from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from store.models import *

# register.html için kullanıcı kayıt formu alanları


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Kullanıcı adı',
                                               'aria-describedby': 'usernameInput', }),

            'email': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'E-Posta',
                                            'aria-describedby': 'emailInput', }),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Adı',
                                                 'aria-describedby': 'fistnameInput', }),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Soyadı',
                                                'aria-describedby': 'lastnameInput', }),

        }


# account-settings.html sayfasındaki müşteri profil alanları


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

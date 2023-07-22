from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from shop.models import CustomUser


class CustomAuthenticationForm(UserCreationForm):
    username = forms.CharField(label='Номер телефона', widget=forms.TextInput(
        attrs={'class': 'form-control  cake__textinput', 'placeholder': 'Номер телефона'}
    ))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control  cake__textinput', 'placeholder': 'Пароль',
               }
    ))
    password2 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control  cake__textinput', 'placeholder': 'Пароль',
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    # def save(self, commit=True):
    #     user = super(CustomAuthenticationForm, self).save(commit=False)
    #     user.username = self.cleaned_data['username']
    #     user.password = self.cleaned_data['password1']
    #     if commit:
    #         user.save()
    #     return user

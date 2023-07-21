from django import forms
from django.contrib.auth import authenticate


class CustomLoginForm(forms.Form):
    username = forms.CharField()

    error_messages = {
        'invalid_login': "Please enter a correct phone number.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean(self):
        username = self.cleaned_data.get('username')

        if username is not None:
            self.user_cache = authenticate(username=username)

        if self.user_cache is None:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
            )

        elif not self.user_cache.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

        return self.cleaned_data

    def get_user(self):
        return self.user_cache




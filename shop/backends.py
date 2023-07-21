from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend, ModelBackend

from shop.models import CustomUser


class LoginBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(phone_number=username)
            return user
        except CustomUser.DoesNotExist:
            return None



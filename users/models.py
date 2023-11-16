from django.contrib.auth.models import AbstractUser
from dry.models import UserMixin


class User(AbstractUser, UserMixin):
    pass

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class User(AbstractUser):
    fullname = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ('fullname', )

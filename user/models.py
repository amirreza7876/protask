from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from user.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True, null=True)
    email = models.EmailField(max_length=300, unique=True)
    username = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

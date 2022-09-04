from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password, **other_fields):
        if not email:
            return ValueError(_("email is required."))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            ValueError(_('superuser must be assign to is_staff=True'))

        if other_fields.get('is_superuser') is not True:
            ValueError(_('superuser must be assign to is_superuser=True'))

        return self.create_user(email, username, password, **other_fields)

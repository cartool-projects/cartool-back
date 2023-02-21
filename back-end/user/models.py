from typing import List

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

from user.validators import validate_phone_number, validate_email, validate_last_name, validate_first_name


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None

    phone_number = models.CharField(
        _('ტელეფონის ნომერი'),
        max_length=20,
        unique=True,
        validators=[validate_phone_number])
    email = models.EmailField(_('იმეილი'), blank=True, unique=True, validators=[validate_email])
    first_name = models.CharField(_('სახელი'), max_length=30, blank=True, validators=[validate_first_name])
    last_name = models.CharField(_('გვარი'), max_length=30,
                                 blank=True,
                                 validators=[validate_last_name], )

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS: List[str] = []

    class Meta:
        verbose_name = _('მომხმარებელი')
        verbose_name_plural = _('მომხმარებლები')

    def set_active(self):
        self.is_active = True
        self.save(update_fields=['is_active'])

    @property
    def full_phone_number(self):
        return f'995{self.phone_number}'

    @property
    def phone_last_three_numbers(self):
        return self.phone_number[-3:]

    def __str__(self) -> str:
        return f'{self.first_name}'

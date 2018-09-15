from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django_extensions.db.fields import ShortUUIDField


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    slug = ShortUUIDField()
    email = models.EmailField(_('email'), unique=True)
    phone = models.CharField(_('phone'), max_length=100, blank=True, null=True)
    forget_password_link = models.CharField(_('forget_password_link'), max_length=200, blank=True, null=True, unique=True)
    forget_password_status = models.BooleanField(default=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    created = models.DateTimeField(_('created'), blank=True, editable=False,
                                   default=timezone.now)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    is_active = models.BooleanField(_('is active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return '{}'.format(self.get_full_name() if self.get_full_name()
                           else self.email.split('@')[0])

    def get_full_name(self):
        "Returns the first_name plus the last_name, with a space in between."
        full_name = u'%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.get_full_name() if self.get_full_name() else self.email.split('@')[0]

    @classmethod
    def create_user(cls, first_name, last_name, email, phone, password):
        cls.objects.create_user(email, password, first_name=first_name, last_name=last_name, phone=phone)


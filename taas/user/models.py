import logging

from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from random import sample

from model_utils import FieldTracker

logger = logging.getLogger(__name__)

phone_regex = RegexValidator(regex=r'^\+?\d{5,15}$', message=_('Phone number is invalid.'))


class CustomUserManager(UserManager):
    def _create_user(self,  email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), unique=True,)
    phone_number = models.CharField(_('phone number'), max_length=15, validators=[phone_regex])
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                    'active. Unselect this instead of deleting accounts.'))
    budget = models.DecimalField(_('budget (€)'), decimal_places=2, max_digits=10,
                                 validators=[MinValueValidator(0.0)], default=0.0)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    pin = models.CharField(_('pin'), max_length=4, blank=True, null=True, )
    button_id = models.CharField(_('Button ID'), max_length=64, blank=True, null=True, )

    objects = CustomUserManager()
    tracker = FieldTracker()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """"
        Returns the short name for the user.
        """
        return self.first_name

    def display_budget_money(self):
        """
        Displays amount of money in budget
        """
        return '%d€' % self.budget

    def create_pin(self):
        """
        Generates a pin for user
        Only 10000 pins are generated. If you plan on having more users, change this.
        """
        all_pins = set('{0:04}'.format(num) for num in range(0, 10000))
        used_pins = set(User.objects.values_list('pin', flat=True))
        all_pins.difference(used_pins)
        self.pin = sample(all_pins, 1)[0]

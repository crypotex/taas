import logging

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.core import validators
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)

phone_regex = RegexValidator(regex=r'^\+?\d{5,15}$', message=_('Phone number is invalid.'))


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True,
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')],
                                error_messages={'unique': _("A user with that username already exists.")})
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'))
    phone_number = models.CharField(_('phone number'), max_length=15, validators=[phone_regex], blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

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

    def email_user_on_registration(self):
        """
        Sends an email to this user, when he is created.
        """
        message = settings.USER_REGISTRATION_MESSAGE
        message = message % {'username': self.username}
        subject = settings.REGISTRATION_SUBJECT
        from_email = settings.EMAIL_HOST_USER

        send_mail(subject, message, from_email, [self.email])
        logger.info('Registration message for user with username %s has been sent.' % self.username)

    def email_user_on_activation(self):
        """
        Sends an email to this user, when he is verified.
        """
        message = settings.USER_VERIFICATION_MESSAGE
        message = message % {'username': self.username}
        subject = settings.USER_STATUS_SUBJECT
        from_email = settings.EMAIL_HOST_USER

        send_mail(subject, message, from_email, [self.email])
        logger.info('Registration message for user with username %s has been sent.' % self.username)

    def email_user_on_deactivation(self):
        """
        Sends an email to this user, when he is disabled.
        """
        message = settings.USER_DISABLED_MESSAGE
        message = message % {'username': self.username}
        subject = settings.USER_STATUS_SUBJECT
        from_email = settings.EMAIL_HOST_USER

        send_mail(subject, message, from_email, [self.email])
        logger.info('Registration message for user with username %s has been sent.' % self.username)

    def email_admin_on_registration(self):
        """
        Sends an email to the admin users, when new user was created.
        """
        message = settings.ADMIN_REGISTRATION_MESSAGE
        message = message % {'username': self.username}
        subject = settings.REGISTRATION_SUBJECT
        from_email = settings.EMAIL_HOST_USER
        to_emails = settings.ADMIN_EMAILS

        send_mail(subject, message, from_email, to_emails)
        logger.info('User with username %s registration message has been sent to admin emails: %s.'
                    % (self.username, ', '.join(to_emails)))

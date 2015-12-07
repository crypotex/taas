import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from taas.user import models


logger = logging.getLogger(__name__)


@shared_task
def email_user_on_registration(user_id):
    """
    Sends an email to this user, when he is created.
    :param user_id: id of the User
    """
    user = models.User.objects.get(id=user_id)
    message = settings.USER_REGISTRATION_MESSAGE
    message = message % {'first_name': user.first_name}
    subject = settings.REGISTRATION_SUBJECT
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [user.email])
    logger.info('Registration message for user with email %s has been sent.' % user.email)


@shared_task
def email_user_on_activation(user_id):
    """
    Sends an email to this user, when he is verified.
    :param user_id: id of the User
    """
    user = models.User.objects.get(id=user_id)
    message = settings.USER_VERIFICATION_MESSAGE
    message = message % {'first_name': user.first_name}
    subject = settings.USER_STATUS_SUBJECT
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [user.email])
    logger.info('Activation message for user with email %s has been sent.' % user.email)


@shared_task
def email_user_on_deactivation(user_id):
    """
    Sends an email to this user, when he is disabled.
    :param user_id: id of the User
    """
    user = models.User.objects.get(id=user_id)
    message = settings.USER_DISABLE_MESSAGE
    message = message % {'first_name': user.first_name}
    subject = settings.USER_STATUS_SUBJECT
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [user.email])
    logger.info('Deactivation message for user with email %s has been sent.' % user.email)


@shared_task
def email_admin_on_user_registration(user_id):
    """
    Sends an email to the admin users, when new user was created.
    :param user_id: id of the User
    """
    user = models.User.objects.get(id=user_id)
    message = settings.ADMIN_REGISTRATION_MESSAGE
    message = message % {'email': user.email}
    subject = settings.REGISTRATION_SUBJECT_ADMIN
    from_email = settings.EMAIL_HOST_USER
    to_emails = settings.ADMIN_EMAILS

    send_mail(subject, message, from_email, to_emails)
    logger.info('User with email %s registration message has been sent to admin emails: %s.'
                % (user.email, ', '.join(to_emails)))


@shared_task
def email_admin_on_user_deactivation(user_id):
    """
    Sends an email to the admin users, when new user was deactivated.
    :param user_id: id of the User
    """

    user = models.User.objects.get(id=user_id)
    message = settings.ADMIN_USER_DISABLE_MESSAGE
    message = message % {'email': user.email}
    subject = settings.USER_STATUS_SUBJECT_ADMIN
    from_email = settings.EMAIL_HOST_USER
    to_emails = settings.ADMIN_EMAILS

    send_mail(subject, message, from_email, to_emails)
    logger.info('User with email %s deactivation message has been sent to admin emails: %s.'
                % (user.email, ', '.join(to_emails)))

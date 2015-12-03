import logging

logger = logging.getLogger(__name__)

def send_emails_to_users(sender, instance=None, created=False, **kwargs):
    if created:
        instance.email_user_on_registration()

        if instance.is_active:
            instance.email_user_on_activation()

        return

    old_active = instance.tracker.previous('is_active')
    new_active = instance.is_active

    if (old_active, new_active) == (False, True):
        instance.email_user_on_activation()
    elif (old_active, new_active) == (True, False):
        instance.email_user_on_deactivation()

def check_user_activation(sender, instance=None, created=False, **kwargs):

    old_active = instance.tracker.previous('is_active')
    new_active = instance.is_active

    if (old_active, new_active) == (False, True):
        instance.create_pin()
    elif (old_active, new_active) == (True, False):
        instance.pin = None


def log_user_login(sender, user=None, **kwargs):
    logger.info('User with email %s has been logged in.' % user.email)


def log_user_logout(sender, user=None, **kwargs):
    logger.info('User with email %s has been logged out.' % user.email)


def log_user_login_failed(sender, credentials=None, **kwargs):
    logger.info('User with email %s has failed to log in.' % credentials.get('username'))

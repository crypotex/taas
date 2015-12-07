from django.utils.translation import ugettext_lazy as _

EMAIL_HOST = ''

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

EMAIL_PORT = 587

EMAIL_USE_TLS = True

ADMIN_EMAILS = []

USER_STATUS_SUBJECT = _('User status')

REGISTRATION_SUBJECT = _('User registration')

USER_STATUS_SUBJECT_ADMIN = 'Kasutaja staatus'

REGISTRATION_SUBJECT_ADMIN = 'Kasutaja registreerimine'

USER_REGISTRATION_MESSAGE = _("""Dear %(first_name)s,

You have successfully registered to the Tartu Agility Arenguselts.
Please wait till admin user verifies your account.
You will get notification about that.

Best regards,

Tartu Agility Arenguselts""")

ADMIN_REGISTRATION_MESSAGE = """Lugupeetud Admin,

Kasutaja emailiga %(email)s liitus broneerimissüsteemiga.
Palun aktiveerige tema konto.

Parimate soovidega,

Tartu Agility Arenguselts"""

USER_VERIFICATION_MESSAGE = _("""Dear %(first_name)s,

Your account was successfully verified by the Tartu Agility Arenguselts.
You can login now.

Best regards,

Tartu Agility Arenguselts""")

USER_DISABLE_MESSAGE = _("""Dear %(first_name)s,

Your Tartu Agility Arenguselts user was disabled.
Please contact administrator for further information.

Best regards,

Tartu Agility Arenguselts""")

ADMIN_USER_DISABLE_MESSAGE = """Lugupeetud Admin,

Kasutaja emailiga %(email)s on deaktiveeritud.

Parimate soovidega,

Tartu Agility Arenguselts"""


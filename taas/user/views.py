import logging

from django.contrib import messages
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

from taas.user import forms
from taas.user import models

logger = logging.getLogger(__name__)


class UserRegisterView(SuccessMessageMixin, CreateView):
    success_message = _('User has been successfully registered.')
    success_url = reverse_lazy('homepage')
    template_name = 'user_registration.html'
    model = models.User
    form_class = forms.UserCreationForm

    def form_valid(self, form):
        logger.info('Unverified user with email %s has been successfully registered.'
                    % form.cleaned_data.get('email'))
        return super(UserRegisterView, self).form_valid(form)


def password_reset(request):
    kwargs = {
        'template_name': 'password_reset/form.html',
        'email_template_name': 'password_reset/email.html',
        'subject_template_name': 'password_reset/subject.html',
        'post_reset_redirect': reverse_lazy('homepage')
    }

    if request.user.is_authenticated():
        return HttpResponseNotFound()

    if request.method == 'POST' and request.POST.get('email'):
        messages.add_message(request, messages.SUCCESS, _('Email instructions has been sent.'),
                             fail_silently=True)
    response = auth_views.password_reset(request, **kwargs)

    return response


def password_reset_confirm(request, uidb64=None, token=None):
    template_name = 'password_reset/confirm.html'
    post_reset_redirect = reverse('homepage')
    token_generator = default_token_generator
    set_password_form = SetPasswordForm

    UserModel = get_user_model()
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS,
                                     _('Your password has been set. You may go ahead and log in now.'),
                                     fail_silently=True)
                logger.info('Password for user %s has been reset.'
                            % user.email)
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }

    return TemplateResponse(request, template_name, context)


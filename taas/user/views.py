import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views, get_user_model, update_session_auth_hash, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView, FormView

from taas.reservation.views import get_payment_order, get_payment_mac
from taas.user import forms
from taas.user import mixins
from taas.user import models

logger = logging.getLogger(__name__)


class UserCreateView(CreateView):
    success_message = _('User has been successfully registered.')
    success_url = reverse_lazy('homepage')
    template_name = 'user_registration.html'
    model = models.User
    form_class = forms.UserCreationForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.email_admin_on_user_registration()

        messages.success(self.request, self.success_message)
        logger.info('Unverified user with email %s has been successfully registered.'
                    % form.cleaned_data.get('email'))
        return HttpResponseRedirect(self.get_success_url())


class UserUpdateView(mixins.LoggedInMixin, UpdateView):
    success_message = _('Information has been updated.')
    success_url = reverse_lazy('user_update_form')
    template_name = 'user_update.html'
    model = models.User
    form_class = forms.UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        self.object = form.save()
        update_session_auth_hash(self.request, self.object)

        messages.success(self.request, self.success_message)
        logger.info('User with email %s has been been updated.' % form.cleaned_data.get('email'))
        return HttpResponseRedirect(self.get_success_url())


class UserDeactivateView(mixins.LoggedInMixin, SuccessMessageMixin, FormView):
    success_message = _('User has been deactivated.')
    form_class = forms.UserDeactivateForm
    template_name = 'user_deactivate.html'
    success_url = reverse_lazy('homepage')

    def get_form_kwargs(self):
        kwargs = super(UserDeactivateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        self.request.user.is_active = False
        self.request.user.save()
        self.request.user.email_admin_on_user_deactivation()
        logger.info('User with email %s has been been deactivated.' % form.cleaned_data.get('email'))

        logout(self.request)
        return super(UserDeactivateView, self).form_valid(form)


def password_reset(request):
    kwargs = {
        'template_name': 'password_reset/form.html',
        'email_template_name': 'password_reset/email.html',
        'subject_template_name': 'password_reset/subject.html',
        'post_reset_redirect': reverse_lazy('homepage')
    }

    if request.method == 'POST' and request.POST.get('email'):
        messages.add_message(request, messages.SUCCESS, _('Email instructions has been sent.'),
                             fail_silently=True)
    response = auth_views.password_reset(request, **kwargs)

    return response


def password_reset_confirm(request, uidb64=None, token=None):
    template_name = 'password_reset/confirm.html'
    post_reset_redirect = reverse('homepage')
    token_generator = default_token_generator
    set_password_form = forms.CustomPasswordSetForm

    UserModel = get_user_model()
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
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
                title = _('Password reset unsuccessful')
        else:
            form = set_password_form(user)
            title = _('Enter new password')
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


class AddBalanceView(mixins.LoggedInMixin, SuccessMessageMixin, FormView):
    form_class = forms.AddBalanceForm
    template_name = 'update_budget.html'

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        payment = get_payment_order(amount, 'B%s' % self.request.user.id)
        mac = get_payment_mac(payment)
        host = settings.MAKSEKESKUS['host']
        return render_to_response('proceed_budget.html', {'json': payment, 'mac': mac, 'host': host})

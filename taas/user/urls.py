from django.conf.urls import url
import django.contrib.auth.views as auth_views
from django.views.generic import TemplateView

from taas.user import views, mixins

urlpatterns = [
    url(r'^register/$', views.UserCreateView.as_view(), name='user_registration_form'),
    url(r'^update/$', views.UserUpdateView.as_view(), name='user_update_form'),
    url(r'^deactivate/$', views.UserDeactivateView.as_view(), name='user_deactivate_form'),
    url(r'^login/$', mixins.logout_required(auth_views.login), {'template_name': 'login.html'}, name='user_login_form'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='user_logout'),
    url(r'^balance/$', views.AddBalanceView.as_view(), name="user_balance"),
    url(r'^terms/$', TemplateView.as_view(template_name='terms.html')),
    url(r'^payment_conditions/$', TemplateView.as_view(template_name='payment_conditions.html')),
    url(r'^privacy_policy/$', TemplateView.as_view(template_name="privacy_policy.html")),

    # password reset related urls
    url(r'^password/reset/$', mixins.logout_required(views.password_reset), name='password_reset'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm')
]

from django.conf.urls import url
import django.contrib.auth.views as auth_views

from taas.user import views

urlpatterns = [
    url(r'^register/$', views.UserRegisterView.as_view(), name='user_registration_form'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='user_login_form'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='user_logout'),

    # password reset related urls
    url(r'^password/reset/$', views.password_reset, name='password_reset'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm')
]

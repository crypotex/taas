from django.conf.urls import url

from .views import UserRegisterView

urlpatterns = [
    url(r'^register/$', UserRegisterView.as_view(), name='user_registration_form'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='user_login_form'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='user_logout'),
]

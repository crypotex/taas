from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^register/$', 'taas.user.views.register_user', name='user_registration_form'),
    url(r'^register/success/$', TemplateView.as_view(template_name='registration_success.html')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    url(r'^login/success/$', TemplateView.as_view(template_name='login_success.html'))
]

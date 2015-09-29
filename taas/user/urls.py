from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^register/$', 'taas.user.views.register_user', name='user_registration_form'),
    url(r'^register/success/$', TemplateView.as_view(template_name='registration_success.html')),
]

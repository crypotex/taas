from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

admin.site.site_header = _('TAAS administration')

urlpatterns = patterns(
    '',
    url(r'^', TemplateView.as_view(template_name='base.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('taas.user.urls')),
)

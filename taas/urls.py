from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


admin.site.site_header = _('TAAS administration')

urlpatterns = patterns(
    '',
    url(r'^', include('taas.templates.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('taas.user.urls')),
)

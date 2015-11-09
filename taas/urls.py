from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from taas.reservation.views import HomePageView


admin.site.site_header = _('TAAS administration')

urlpatterns = patterns(
    '',
    url(r'^$', HomePageView.as_view(), name='homepage'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('taas.user.urls')),
    url(r'^reservation/', include('taas.reservation.urls'))
)

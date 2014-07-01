from django.conf.urls import patterns, include, url
from django.contrib.sitemaps import FlatPageSitemap

from django.contrib import admin
admin.autodiscover()

from referrals.sitemaps import ReferralSitemap

sitemaps = {
        'referrals': ReferralSitemap,
        'pages': FlatPageSitemap,
}


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'referiend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('userprofile.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^referrals/', include('referrals.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^$', 'homepage.views.homepage', name='home'),
)

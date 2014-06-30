from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'referiend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('userprofile.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'', include('referrals.urls')),
    url(r'^$', 'homepage.views.homepage', name='home'),
    url(r'search/', include('search.urls')),
)

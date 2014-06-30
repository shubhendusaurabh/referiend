from django.conf.urls import patterns, url

urlpatterns = patterns('search.views',

        url(
            regex   = '^$',
            view    = 'search',
            name    = 'search'
        ),

        url(
            regex   = '^referrals/autocomplete/$',
            view    = 'search_referrals_autocomplete',
            name    = 'search_referrals_autocomplete'
        ),
)

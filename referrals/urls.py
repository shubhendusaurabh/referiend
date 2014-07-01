from django.conf.urls import patterns, url
from django.views.generic.dates import ArchiveIndexView

from referrals.models import Referral
from referrals.feeds import AtomLatestReferralsFeed, RssLatestReferralsFeed
import views

urlpatterns = patterns('referrals.views',
        url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', 'referraldetail', name='referral_detail'),
        url(r'^add/$', views.referralcreate, name='referral_add'),
        url(r'^edit/(?P<pk>\d+)/$', views.referralupdate, name='referral_update'),
        url(r'^delete/(?P<pk>\d+)/$', views.referraldelete, name='referral_delete'),
        url(r'^$', 'referrallist', name='referral_list'),
        url(r'^user/(?P<username>\w+)/$', views.userreferrallist, name='user_referral_list'),
        
        url(
            regex=r"^latest/$",
            view=ArchiveIndexView.as_view(
                queryset=Referral.objects.filter().select_related(),
                paginate_by=50,
                date_field="updated_at"
            ),
            name='referral_archive',
        ),

        # Feeds
        url(
            regex=r'^latest/rss/$',
            view=RssLatestReferralsFeed(),
            name='feeds_latest_referrals_rss'
        ),
        url(
            regex=r'^latest/atom/$',
            view=AtomLatestReferralsFeed(),
            name='feeds_latest_referrals_atom'
        ),

        url(
            regex=r'^category/(?P<slug>[\w-]+)/$',
            view='categorydetail',
            name='category'
        ),
        url(
            regex=r'^categories/$',
            view='categorylist',
            name='categories'
        ),

        url(
            regex=r'^vote/$',
            view='yayOrNay',
            name='yayornay'
        ),
)

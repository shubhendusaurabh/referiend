from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from referrals.models import Referral


class RssLatestReferralsFeed(Feed):
    title = 'Latest Referrals Added'
    link = '/referrals/latest/'
    description = 'The last 15 referrals added'

    def items(self):
        return Referral.objects.all().order_by('-created_at')[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.info

    def item_pubdate(self, item):
        return item.created_at


class AtomLatestReferralsFeed(RssLatestReferralsFeed):
    feed_type = Atom1Feed
    subtitle = RssLatestReferralsFeed.description

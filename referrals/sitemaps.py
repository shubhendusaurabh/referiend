from django.contrib.sitemaps import Sitemap, FlatPageSitemap

from .models import Referral

class ReferralSitemap(Sitemap):

    def items(self):
        return Referral.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

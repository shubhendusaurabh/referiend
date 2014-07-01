from django.contrib.sitemaps import Sitemap, FlatPageSitemap

from .models import Referral

class ReferralSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Referral.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

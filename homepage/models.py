import datetime

from django.db import models

from referrals.models import Referral
from core.models import TimeStampedModel


class RotatorManager(models.Manager):

    def get_current(self):
        now = datetime.datetime.now()
        return self.get_queryset().filter(start_date__lte=now, end_date__gte=now)

class Rotw(TimeStampedModel):

    referral = models.ForeignKey(Referral)
    start_date = models.DateField("Start Date")
    end_date = models.DateField("End Date")

    objects = RotatorManager()

    class Meta:
        ordering = ('-start_date', '-end_date',)
        get_latest_by = 'created_at'

        verbose_name = "Referral of the Week"
        verbose_name_plural = 'Referrals of the Week'

    def __unicode__(self):
        return '%s : %s - %s' % (self.referral.title, self.start_date, self.end_date)

    @models.permalink
    def get_absolute_url(self):
        return ('referral_detail', [self.referral.pk, self.referral.slug])


class PSA(TimeStampedModel):
    '''Public Service Annoucement'''

    body_text = models.TextField('Body Text', blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = 'created_at'

        verbose_name = 'Public Service Announcement'
        verbose_name_plural = 'Public Service Announcements'

    def __unicode__(self):
        return '{0} : {1}'.format(self.created_at, self.body_text)
            

# Create your models here.

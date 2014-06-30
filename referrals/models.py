import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify

from core.models import TimeStampedModel

class Category(TimeStampedModel):
    title = models.CharField('Title', max_length=50)
    slug = models.SlugField('Slug')
    description = models.TextField('Description', blank=True)
    title_plural = models.CharField('Title Plural', max_length=50, blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('category', [self.slug])


class Referral(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, help_text='Enter a valid slug consisting of numbers, underscores or hyphens.', unique=True, blank=True, null=True)
    url = models.URLField(null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(User, related_name='referrer')
    info = models.TextField() #maybe markdown enabled

    view_count = models.PositiveIntegerField(default=0)

    company = models.CharField(max_length=255) # either make it foreign key for better searches or tagging based

    yay = models.PositiveIntegerField(default=1)
    nay = models.PositiveIntegerField(default=0)

    expired = models.BooleanField(default=0)
    validity = models.DateField(null=True, blank=True, default=(timezone.now().date() + datetime.timedelta(days=90)))

    category = models.ForeignKey(Category, verbose_name='Category')
    usage = models.ManyToManyField(User, blank=True, related_name='referee')
    # logo = models.ImageField() # company has a logo not a referral

    def get_usage_count(self):
        return self.usage.count()

    @property
    def is_active(self):
        return not self.expired

    def set_expired_status(self):
        self.expired = True
        self.save()

    # TODO Code Smells
    def update_view_count(self):
        self._increment_and_save('view_count')

    def yayornay(self, opinion, user):
        if user.is_authenticated():
            self.usage.add(user)
        self._increment_and_save(opinion)

    def _increment_and_save(self, attr):
        if hasattr(self, attr):
            setattr(self, attr, getattr(self, attr, 0) + 1)
        self.save()

    class Meta:
        ordering = ['updated_at']

    @models.permalink
    def get_absolute_url(self):
        return 'referral_detail', (), {'pk': self.pk, 'slug': self.slug}

    def __unicode__(self):
        if self.url:
            return '%s -> %s' % ( self.url, self.author )
        elif self.code:
            return '%s -> %s' % (self.code, self.author)

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User

from allauth.account.signals import user_signed_up

from core.models import TimeStampedModel

class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, related_name='profile')
    email = models.EmailField('Email', null=True, blank=True) # not needed may be

    class Meta:
        verbose_name = 'User Profile'

    @models.permalink
    def get_absolute_url(self):
        # TODO:: use username rather than id
        return ('userprofile_detail', [self.user.pk])

    #def avatar_image(self):
        #return (MEDIA_URL + self.avatar.name) if self.avatar else None

    def __unicode__(self):
        # TODO:: what if user registers through social accounts
        return self.user.username

    def save(self, **kwargs):
        '''
        Override save to always populate email changes to auth.user.model
        '''
        if self.email is not None:
            email = self.email.strip()
            user_obj = User.objects.get(username=self.user.username)
            user_obj.email = email
            user_obj.save()

        super(UserProfile, self).save(**kwargs)


@receiver(user_signed_up)
def create_userprofile(sender, **kwargs):
    request = kwargs['request']
    user = kwargs['user']
    
    obj, created = UserProfile.objects.get_or_create(user=user, email=user.email)
    
    
from django import template

register = template.Library()

@register.filter
def referral_usage(user):
    return user.referral_set.all()

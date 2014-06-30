from django import template
from django.contrib.flatpages.models import FlatPage

register = template.Library()

@register.inclusion_tag('footer.html')
def footer_links():
    flatpages = FlatPage.objects.all()
    return { 'flatpages': flatpages }


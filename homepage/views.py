from random import sample

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from homepage.models import Rotw, PSA
from referrals.models import Referral, Category

def homepage(request, template_name='homepage.html'):
    categories = []
    for category in Category.objects.annotate(referral_count=Count('referral')):
        element = {
                'title': category.title,
                'description': category.description,
                'count': category.referral_count,
                'slug': category.slug,
                'title_plural': category.title_plural,
            }
        categories.append(element)

    # get upto 5 random referrals
    referral_count = Referral.objects.count()
    random_referrals = []
    if referral_count > 1:
        referral_ids = set([])

        # get 5 random keys
        referral_ids = sample(
                range(1, referral_count + 1), # generate a list from 1 to referral_count+1
                min(referral_count, 5) # get a sample of the smaller of 5 or the referra count
        )

        # Get the random packages
        random_referrals = Referral.objects.select_related().filter(pk__in=referral_ids)[:5]

    try:
        rotw = Rotw.objects.select_related().latest().referral
    except Rotw.DoesNotExist:
        rotw = None
    except Referral.DoesNotExist:
        rotw = None

    # service announcements on homepage
    try:
        psa_body = PSA.objects.latest().body_text
    except PSA.DoesNotExist:
        psa_body = '<p>There are currently no announcements.</p>'

    # TODO latest blog posts on homepage

    return render(request,
            template_name, {
                'latest_referrals': Referral.objects.select_related().all().order_by('-created_at')[:5],
                'random_referrals': random_referrals,
                'rotw': rotw,
                'psa_body': psa_body,
                'categories': categories,
                'referral_count': referral_count,
            }
    )

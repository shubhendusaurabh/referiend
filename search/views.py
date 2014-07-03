import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q

from .forms import SearchForm 
from referrals.models import Referral


def search_function(q):
    # todo return all if empty q and check company
    items = []
    if q:
        items = Referral.objects.select_related().filter(
                Q(title__icontains=q) |
                Q(slug__startswith=q.lower()) |
                Q(info__icontains=q) )
    else:
        items = Referral.objects.select_related()
    return items
def search(request):

    q = request.GET.get('q', '')
    template_name = 'search/search.html'

    if '/' in q:
        lst = q.split('/')
        try:
            if lst[-1]:
                q = lst[-1]
            else:
                q = lst[-2]
        except IndexError:
            pass

    try:
        referral = Referral.objects.get(title=q)
        url = referral.get_absolute_url()
        return HttpResponseRedirect(url)
    except Referral.DoesNotExist:
        pass
    except Referral.MultipleObjectsReturned:
        pass

    try:
        referral = Referral.objects.get(slug=q)
        url = referral.get_absolute_url()
        return HttpResponseRedirect(url)
    except Referral.DoesNotExist:
        pass
    except Referral.MultipleObjectsReturned:
        pass

    form = SearchForm(request.GET or None)

    return render(request, template_name, { 'referrals': search_function(q), 'form': form })


def search_referrals_autocomplete(request):
    q = request.GET.get('term', '')
    if q:
        objects = search_function(q)[:15]
        objects = objects.values_list('title', flat=True)
        json_response = json.dumps(list(objects))
    else:
        json_response = json.dumps([])

    return HttpResponse(json_response, mimetype='text/javascript')

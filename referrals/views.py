from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django.utils.text import slugify
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.views import LoginRequiredMixin, UserCheckMixin

import models
from referrals.models import Category, Referral
from homepage.models import Rotw
import forms

class ReferralList(ListView):
    model = models.Referral

    def get_context_data(self, *args, **kwargs):
        context = super(ReferralList, self).get_context_data(*args, **kwargs)
        #context['categories'] = Category.objects.annotate(referral_count=Count('referral'))
        #context['rotw'] = Rotw.objects.get_current()
        categories = []
        for category in Category.objects.select_related().annotate(referral_count=Count('referral')):
            element = {
                'title': category.title,
                'description': category.description,
                'slug': category.slug,
                'title_plural': category.title_plural,
                'referral_count': category.referral_count,
                'referrals': category.referral_set.select_related().annotate(usage_count=Count('usage'))[:5]
            }
            categories.append(element)
        context['categories'] = categories
        return context
referrallist = ReferralList.as_view()

class UserReferralList(ListView):
    template_name = 'referrals/user_referral_list.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        queryset = models.Referral.objects.select_related().filter(author=self.user).annotate(usage_count=Count('usage'))
        return queryset
    # currently not being used
    def get_context_data(self, **kwargs):
        context = super(UserReferralList, self).get_context_data(**kwargs)
        context['author'] = self.user
        return context
userreferrallist = UserReferralList.as_view()

class ReferralDetail(DetailView):
    model = models.Referral
    def get_context_data(self, *args, **kwargs):
        context = super(ReferralDetail, self).get_context_data(*args, **kwargs)
        pk = self.kwargs['pk']
        context['referral'] = Referral.objects.select_related().get(pk=pk)
        return context
    #TODO blocking request
    def get_object(self):
        object = super(ReferralDetail, self).get_object()
        object.view_count += 1
        object.save()
        return object
referraldetail = ReferralDetail.as_view()

class ReferralCreate(LoginRequiredMixin, CreateView):
    model = models.Referral
    form_class = forms.ReferralForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.title) #TODO make it user editable or some other logic to make it unique
        self.object.author = self.request.user
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS, 'Referral added successfully')
        return redirect(self.object)
referralcreate = ReferralCreate.as_view()

class ReferralUpdate(LoginRequiredMixin, UserCheckMixin, SuccessMessageMixin, UpdateView):
    model = models.Referral
    form_class = forms.ReferralForm
    success_message = "%(title)s updated successfully"    
referralupdate = ReferralUpdate.as_view()

class ReferralDelete(LoginRequiredMixin, UserCheckMixin, DeleteView):
    model = models.Referral
    def get_success_url(self):
        messages.add_message(self.request, messages.WARNING, 'Referral deleted successfully')
        return reverse('referral_list')
referraldelete = ReferralDelete.as_view()


class CategoryDetail(DetailView):
    model = Category
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetail, self).get_context_data(*args, **kwargs)
        context['referrals'] = self.object.referral_set.select_related().annotate(usage_count=Count('usage')).order_by('title')
        return context
categorydetail = CategoryDetail.as_view()


class CategoryList(ListView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryList, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.select_related().annotate(referral_count=Count('referral'))
        return context
categorylist = CategoryList.as_view()




def yayOrNay(request):
    success = False
    referral = get_object_or_404(Referral, id=request.POST['id'])
    url = referral.get_absolute_url()
    if request.POST.has_key('yay'):
        referral.yayornay('yay', request.user)
    elif request.POST.has_key('nay'):
        referral.yayornay('nay', request.user)

    messages.add_message(request, messages.INFO, 'Thanks! For your Feedback. It is very helpful for other users')

    if request.is_ajax():
        response = {}
        response['success'] = True
        return HttpResponse(json.dumps(response))
    return HttpResponseRedirect(url)

from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from core.views import LoginRequiredMixin

from userprofile.models import UserProfile
from userprofile.forms import UserProfileForm


class UserProfileDetail(DetailView):
    model = UserProfile
userprofile_detail = UserProfileDetail.as_view()


class UserProfileList(ListView):
    template_name = 'userprofile/userprofile_list.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            self.users = User.objects.all()
        else:
            self.users = User.objects.filter(is_active=True)
        return self.users

    def get_context_data(self, **kwargs):
        context = super(UserProfileList, self).get_context_data(**kwargs)
        context['users'] = self.users
        return context
userprofile_list = UserProfileList.as_view()


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'userprofile/userprofile_edit.html'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.INFO, 'Profile Saved')
        return HttpResponseRedirect(reverse('userprofile_detail', kwargs={'pk': self.get_object().pk}))
userprofile_edit = UserProfileUpdateView.as_view()

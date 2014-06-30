import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.views.generic.detail import SingleObjectMixin

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class UserCheckMixin(SingleObjectMixin):

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return HttpResponseForbidden()
        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)


class AjaxableResponseMixin(object):
    '''
    Mixin to add AJAX support to a form.
    Must be used with a object-based FormView
    '''
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                    'pk': self.object.pk,
                }
            return self.render_to_json_response(data)
        else:
            return response

import requests
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse

from links.models import Link
from links.forms import LinkForm


class LinkListView(LoginRequiredMixin, ListView):
    template_name = 'links/links_list.html'
    model = Link
    paginate_by = 20

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user).order_by('-created')


class LinkAddFormView(LoginRequiredMixin, CreateView):
    template_name = 'links/links_add.html'
    form_class = LinkForm

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        return super(LinkAddFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('links:links-list')


class LinkDeleteFormView(LoginRequiredMixin, DeleteView):
    model = Link

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user) #.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('links:links-list')


@login_required
def check(request, pk):
    if not pk:
        return HttpResponseBadRequest(
            json.dumps({'error': '`url` param is not provided in url.'}), 
            content_type="application/json"
        )

    link = Link.objects.filter(user=request.user, pk=pk).first()
    if not link:
        raise Http404

    status_code = -1
    try:
        response = requests.get(link.url)
        status_code = response.status_code
    except requests.ConnectionError:
        pass

    return HttpResponse(
        json.dumps({'status': status_code, 'pk': link.pk}), 
        content_type="application/json"
    )


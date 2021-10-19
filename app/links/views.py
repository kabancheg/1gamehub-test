import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
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
        return Link.objects.all().order_by('-created') #.filter(user=self.request.user)


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

    def get_success_url(self):
        return reverse('links:links-list')


def check(request):
    url = request.GET.get('url', None)
    if not url:
        return HttpResponseBadRequest(
            json.dumps({'error': '`url` param is not provided in url.'}), 
            content_type="application/json"
        )

    import requests
    try:
        response = requests.get(url)
        status_code = response.status_code
    except requests.ConnectionError:
        status_code = -1

    return HttpResponse(
        json.dumps({'status': status_code, 'url': url}), 
        content_type="application/json"
    )


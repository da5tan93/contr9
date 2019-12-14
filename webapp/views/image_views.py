from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from webapp.forms import ImageForm, ImageCommentForm
from webapp.models import Image


class IndexView(ListView):
    context_object_name = 'images'
    model = Image
    template_name = 'base/index.html'
    ordering = ['-created_at']
    paginate_by = 5
    paginate_orphans = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class ImageView(DetailView):
    template_name = 'base/image.html'
    model = Image
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ImageCommentForm()
        comments = context['image'].comments.order_by('-created_at')
        self.paginate_comments_to_context(comments, context)
        return context

    def paginate_comments_to_context(self, comments, context):
        paginator = Paginator(comments, 3, 0)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['comments'] = page.object_list
        context['is_paginated'] = page.has_other_pages()


class ImageCreateView(CreateView):
    model = Image
    template_name = 'base/create.html'
    form_class = ImageForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('webapp:accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:image_view', kwargs={'pk': self.object.pk})


class ImageUpdateView(LoginRequiredMixin, UpdateView):
    model = Image
    template_name = 'base/update.html'
    context_object_name = 'image'
    form_class = ImageForm

    def get_success_url(self):
        return reverse('webapp:image_view', kwargs={'pk': self.object.pk})


class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = Image
    template_name = 'base/delete.html'
    context_object_name = 'image'
    success_url = reverse_lazy('webapp:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.save()
        return redirect(self.get_success_url())

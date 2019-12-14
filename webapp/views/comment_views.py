from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, \
    UpdateView, DeleteView
from webapp.forms import CommentForm, ImageCommentForm
from webapp.models import Comment, Image


User = get_user_model()


def add_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Comment.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, author=user)
    return like


def remove_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    Comment.objects.filter(
        content_type=obj_type, object_id=obj.id, author=user
    ).delete()


def is_fan(obj, user) -> bool:
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Comment.objects.filter(
        content_type=obj_type, object_id=obj.id, author=user)
    return likes.exists()


def get_fans(obj):
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)


class CommentListView(ListView):
    context_object_name = 'comments'
    model = Comment
    template_name = 'comment/list.html'
    ordering = ['-created_at']
    paginate_by = 10
    paginate_orphans = 3


class CommentForImageCreateView(LoginRequiredMixin, CreateView):
    template_name = 'comment/create.html'
    form_class = ImageCommentForm

    def dispatch(self, request, *args, **kwargs):
        self.image = self.get_image()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.image.comments.create(**form.cleaned_data)
        return redirect('webapp:image_view', pk=self.image.pk)

    def get_image(self):
        image_pk = self.kwargs.get('pk')
        return get_object_or_404(Image, pk=image_pk)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment/create.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('webapp:image_view', kwargs={'pk': self.object.image.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:image_view', kwargs={'pk': self.object.image.pk})

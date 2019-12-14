from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Comment(models.Model):
    text = models.TextField(max_length=400, null=False, blank=False, verbose_name='Текст')
    image = models.ForeignKey('webapp.Image', related_name='comments', on_delete=models.CASCADE,
                              verbose_name='Фотография')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE,
                               verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.text[:20]


class Image(models.Model):
    image = models.ImageField(upload_to='product_images', null=False, blank=True, verbose_name='Фотография')
    sign = models.CharField(max_length=200, null=False, blank=False, verbose_name='Подпись')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    likes = GenericRelation(Comment, default=0)
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return str(self.image)

    @property
    def total_likes(self):
        return self.likes.count()
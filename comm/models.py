from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models


class Comment(models.Model):
    text = models.TextField(max_length=200, null=False, blank=False, verbose_name='Текст')
    ftg = models.ForeignKey('webapp.Image', related_name='comments', on_delete=models.CASCADE, verbose_name='Фотография')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE,
                             verbose_name='Автор')
    date_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата-время создания')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
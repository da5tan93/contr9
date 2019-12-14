from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from comm.models import Comment


class Image(models.Model):
    image = models.ImageField(upload_to=None, blank=False, verbose_name='Фотография')
    sign = models.CharField(max_length=200, null=False, blank=False, verbose_name='Подпись')
    date_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата-время создания')
    likes = GenericRelation(Comment, default=0)
    author = models.ForeignKey(User, null=False, blank=False, verbose_name='Автор')

    def __str__(self):
        return self.sign

    @property
    def total_likes(self):
        return self.likes.count()

# Create your models here.

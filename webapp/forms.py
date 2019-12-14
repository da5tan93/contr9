from django import forms
from django.core.exceptions import ValidationError

from webapp.models import Image, Comment


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['created_at', 'updated_at']

    def clean_sign(self):
        sign = self.cleaned_data['sign']
        if len(sign) <= 3:
            raise ValidationError('This field value should be more than 3 symbols long.',
                                  code='too_short')
        return sign


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['created_at', 'updated_at']


class ImageCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
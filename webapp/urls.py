from django.urls import path
from webapp.views.base_views import ListView, TemplateView
from webapp.views.image_views import ImageView, ImageCreateView, ImageUpdateView, ImageDeleteView
from webapp.views.comment_views import CommentCreateView, CommentForImageCreateView, CommentListView, CommentDeleteView
from webapp.views.image_views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('image/<int:pk>/', ImageView.as_view(), name='image_view'),
    path('image/add/', ImageCreateView.as_view(), name='image_add'),
    path('image/<int:pk>/edit/', ImageUpdateView.as_view(), name='image_update'),
    path('image/<int:pk>/delete/', ImageDeleteView.as_view(), name='image_delete'),
    path('comments/', CommentListView.as_view(), name='comment_list'),
    path('comment/add/', CommentCreateView.as_view(), name='comment_add'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('image/<int:pk>/add-comment/', CommentForImageCreateView.as_view(), name='image_comment_create')
]


app_name = 'webapp'

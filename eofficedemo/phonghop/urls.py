from django.urls import path
from . import views
# from .views import PostListView, PostDetailView, home, post, like,dislike, list, AddPost
urlpatterns = [
    path('', views.phonghop, name='phonghop'),
    path('<int:pk>/', views.chitietphonghop, name='chitietphonghop'),
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    path('dangkyphonghop/<int:pk>/', views.EditPost, name='dangkyphonghop'),
    path('posts/', views.get_posts, name='get_posts'),
    # path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('api/get_post/<int:post_id>/', views.get_post, name='get_post'),
]
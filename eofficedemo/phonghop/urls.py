from django.urls import path
from . import views
# from .views import PostListView, PostDetailView, home, post, like,dislike, list, AddPost
urlpatterns = [
    path('', views.phonghop, name='phonghop'),
    path('<int:pk>/', views.chitietphonghop, name='chitietphonghop'),
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    path('dangkyphonghop/<int:pk>/', views.EditPost, name='dangkyphonghop'),
    
]
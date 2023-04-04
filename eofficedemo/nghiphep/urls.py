from django.urls import path
from . import views
# from .views import PostListView, PostDetailView, home, post, like,dislike, list, AddPost
urlpatterns = [
    path('', views.list, name='blog'),
    path('addpost', views.AddPost, name='addpost'),
    path('editpost/<int:pk>/', views.EditPost, name='editpost'),
#     path('blog', list, name='blog'),
#     # path('<int:id>/', detail, name='post_detail'),
#     path('', home, name='home'),
#     # path('blog', PostListView.as_view(), name='blog'),
    path('<int:pk>/', views.post, name='post_detail'),
    path('like/', views.like, name='likepost'),
    path('dislike/', views.dislike, name='dislikepost'),
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('', views.login_user, name='login'),
    path('createprofile', views.CreateProfile, name='createprofile'),
    path('editprofile', views.EditProfile, name='editprofile'),
    path('editprofile/<int:pk>/', views.EditProfileAll, name='profiledetail'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('staff', views.UserListView.as_view(), name='staff'),
    path('search', views.search_venues, name='search-venues'),
    path('upload', views.simple_upload, name='upload'),
]
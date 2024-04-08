from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListAPIView.as_view(), name='post-list'),
    path('<slug:slug>/', views.PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/delete/', views.PostDeleteAPIView.as_view(), name='post-delete'),
    path('posts/create/', views.PostCreateView.as_view(), name = 'post-create'),
    path('posts/<slug:slug>/edit/', views.PostEditView.as_view(), name='post-edit'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("posts/signup/", views.user_signup, name="signup"),
    path('posts/<slug:slug>/comment/', views.CommentCreateView.as_view(), name='comment'),
]


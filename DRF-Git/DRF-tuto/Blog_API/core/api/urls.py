from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'userprofiles', views.UserProfileViewSet, basename='userprofile')
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'tags', views.TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
]
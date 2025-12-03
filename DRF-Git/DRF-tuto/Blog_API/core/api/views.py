from django.shortcuts import render
from .models import Book, Task, Author, Product, CustomUser, UserProfile, Post, Tag , Comments
from .serializers import BookSerializer, TaskSerializer, AuthorSerializer, ProductSerializer, UserRegistrationSerializer, LoginSerializer, UserProfileSerializer, PostSerializer, TagSerializer, CommentSerializer
from rest_framework import viewsets, filters, status, generics
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from .filters import BookFilter, TaskFilter 
from django_filters.rest_framework import DjangoFilterBackend 
from .permissions import IsOwnerOrReadOnly, IsOwnerOnly 
from .throttles import BookCreateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Count 
from .task import send_post_notification

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    throttle_classes = [BookCreateThrottle]
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, ]
    filterset_class = BookFilter
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['title', 'author', 'published_date', 'created_at']
    ordering = ['-created_at']
    pagination_class = PageNumberPagination
    print("Page size:", pagination_class.page_size)

    def perform_create(self, serializer):

        print("User:", self.request.user)
        print("Authenticated:", self.request.user.is_authenticated)

        serializer.save(owner=self.request.user)
        

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed', 'priority', 'category']
    search_fields = ['title', 'desc'] 
    ordering_fields = ['title','priority', 'due_date', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Task.objects.select_related('owner', 'category').prefetch_related(
            'assigned_to'
        ).filter(owner=self.request.user)

        if self.request.query_params.get('overdue') == 'true':
            from django.utils import timezone
            queryset = queryset.filter(due_date__lt=timezone.now(), completed=False)

        return queryset

    def perform_create(self, serializer):
        print("User:", self.request.user)
        print("Authenticated:", self.request.user.is_authenticated)
        serializer.save(owner=self.request.user)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'success_message': 'Authors retrieved successfully',
            'results': serializer.data
        })

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        print("User:", request.user)
        print("Authenticated:", request.user.is_authenticated)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'success_message': 'Products retrieved successfully',
            'results': serializer.data
        })
    

#  User Registration View
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

# login
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        print("User:", self.request.user)
        print("Authenticated:", self.request.user.is_authenticated)
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['published', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related(
            'tags', 'comments', 'comments__author'
        ).annotate(comment_count=Count('comments')).all()
    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class= CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.request.query_params.get('post', None)
        queryset = Comments.objects.select_related('author', 'post').all()

        if post_id is not None:
            queryset =queryset.filter(post__id=post_id)

        return queryset
    
    def perform_create(self, serializer):
        post_id = serializer.validated_data.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
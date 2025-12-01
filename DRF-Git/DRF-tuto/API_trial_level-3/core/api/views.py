from django.shortcuts import render
from .models import Book, Task, Author, Product, CustomUser, UserProfile
from .serializers import BookSerializer, TaskSerializer, AuthorSerializer, ProductSerializer, UserRegistrationSerializer, UserProfileSerializer
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
from .serializers import LoginSerializer


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
        
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)

    #     return Response({
    #         'count': queryset.count(),
    #         'success_message': 'Books retrieved successfully',
    #         'results': serializer.data
    #     })

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    # queryset = Task.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'desc'] 
    ordering_fields = ['title', 'completed', 'created_at']
    ordering = ['-created_at']

    def partial_update(self, request, pk=None):

        print("User:", request.user)
        print("Authenticated:", request.user.is_authenticated)

        if not request.user.has_perm('api.change_task'):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, pk)

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        print("User:", self.request.user)
        print("Authenticated:", self.request.user.is_authenticated)
        serializer.save(owner=self.request.user)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)

    #     return Response({
    #         'count': queryset.count(),
    #         'success_message': 'Tasks retrieved successfully',
    #         'results': serializer.data
    #     })
    

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

        # Generate tokens
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

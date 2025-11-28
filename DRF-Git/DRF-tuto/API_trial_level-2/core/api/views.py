from django.shortcuts import render
from rest_framework.views import exception_handler
from rest_framework import viewsets, filters
from .models import Book, Task, Author, Product, CustomUser
# from django.contrib.auth.models import CustomUser # type: ignore
from .serializers import BookSerializer, TaskSerializer, AuthorSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'success_message': 'Books retrieved successfully',
            'results': serializer.data
        })

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'desc'] 

    ordering_fields = ['title', 'completed', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'success_message': 'Tasks retrieved successfully',
            'results': serializer.data
        })
    

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
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'success_message': 'Products retrieved successfully',
            'results': serializer.data
        })
    
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': {
                'status_code': response.status_code,
                'message': 'An error occurred',
                'details': response.data
            }
        }
        response.data = custom_response_data

    return response

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
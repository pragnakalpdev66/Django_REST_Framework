import django_filters # type: ignore
from .models import Book, Task

class BookFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(lookup_expr='icontains') # lookup_expr for case-insensitive check from db
    published_after = django_filters.DateFilter(field_name='published_date', lookup_expr='gte')
    published_before = django_filters.DateFilter(field_name='published_date', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['author', 'published_after', 'published_before']

class TaskFilter(django_filters.FilterSet):
    # completed = django_filters.BooleanFilter()
    # created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    # created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)

    class Meta:
        model = Task
        # fields = ['completed', 'created_after', 'created_before']
        fields = ['priority']
from django.contrib import admin
from .models import Book, Task, Author

admin.site.register(Book)
admin.site.register(Task)
admin.site.register(Author)
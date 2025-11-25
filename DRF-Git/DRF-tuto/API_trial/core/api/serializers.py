from rest_framework import serializers
from .models import Book, Task, Author, Product
# Create a serializer that: 
# - Includes all fields from Book model 
# - Adds a computed field is_recent (True if created in last 7 days) 
# - Excludes updated_at from response 
# - Makes isbn optional when creating
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    def validate_isbn(self, value):
        if value is None or value == '':
            return value
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be 13 characters long.")
        return value
    
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters")
        return value

    def validate(self, data):
        if data.get('completed') and not data.get('desc'):
            raise serializers.ValidationError("Completed tasks must have a description.")
        return data
    

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
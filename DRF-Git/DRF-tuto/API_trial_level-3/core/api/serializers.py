from rest_framework import serializers # type: ignore
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Book, Task, Author, Product, UserProfile, CustomUser, Post, Tag
from django.contrib.auth import authenticate
from .validators import validate_no_profanity

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            user_obj = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data = super().validate(attrs)
        return data

class BookSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id','owner', 'created_at', 'updated_at']

    def validate_isbn(self, value):
        if value is None or value == '':
            return value
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be 13 characters long.")
        return value
    
    
class TaskSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id','owner', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters")
        return value

    def validate(self, data):
        if data.get('completed') and not data.get('desc'):
            raise serializers.ValidationError("Completed tasks must have a description.")
        return data

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

# custom serializer field 
class AgeField(serializers.IntegerField):
    def to_internal_value(self, data):
        age = super().to_internal_value(data)
        if age < 0 or age > 150:
            raise serializers.ValidationError("Age must be between 0 and 150")
        return age
     
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    age = AgeField()

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

# custom serializer field 
class UppercaseCharField(serializers.CharField):
    def to_representation(self, value):
        return super().to_representation(value).upper() if value else value
    
class PostSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, required=False)
    # comment = CommentSerializer(many=True, read_only=True)
    title = UppercaseCharField()
    content = serializers.CharField(validators=[validate_no_profanity])

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id','suthor', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required to create a post.")
        
        validated_data['author'] = request.user
        tags_data= validated_data.pop('tag', [])

        post = Post.objects.create(author=request.user, **validated_data)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            post.tag.add(tag)

        return post
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        # if tags_data is not None:
        #     instance.tags.clear()
        #     for tag_data in tags_data:
        #         tag, created = Tag.objects.get_or_create(name=tag_data['name'])
        #         instance.tags.add(tag)

        # return instance
    
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.save()
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data['name'])
                instance.tags.add(tag)
        else:
            instance.save()

        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['author_full_name'] = f"{instance.author.first_name} {instance.author.last_name}"
        representation['comment_count'] = instance.comments.count()

        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')

        return representation
    
    def get_author_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_is_author(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False


# # Field-Level Validation
# class PostSerializer(serializers.ModelSerializer):
#     title = serializers.CharField(max_length=200)

#     def validate_title(self, value):
#         if len(value) > 10:
#             raise serializers.ValidationError("Tutle must be at least 10 cjaracters")
#         if 'spam' in value.lower():
#             raise serializers.ValidationError("Title can not containe spam")
#         return value
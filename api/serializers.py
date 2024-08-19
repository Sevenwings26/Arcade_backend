from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, CarouselImage, HomeDisplayShows, UpcomingEvent, Blog
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

# To send token to the frontend 
class MyTOPS(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['bio'] = user.profile.bio
        token['first_name'] = user.profile.first_name
        return token

# Registration serializer 
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Image upload
class CarouselImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = CarouselImage
        fields = ('id', 'title', 'description', 'image')


class DisplayShowsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = HomeDisplayShows
        fields = ('title','image')


class UpcomingEventSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = UpcomingEvent
        fields = ('title', 'image')

class BlogSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Blog
        fields = ('title','image','description','body')
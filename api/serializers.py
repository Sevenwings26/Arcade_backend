from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from .models import User, CarouselImage, HomeDisplayShows, UpcomingEvent, Blog

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

# # Password reset serializer
# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         try:
#             user = User.objects.get(email=value)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("No user is associated with this email address.")
#         return value

#     def save(self, request):
#         user = User.objects.get(email=self.validated_data['email'])
#         token_generator = PasswordResetTokenGenerator()
#         token = token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         domain = get_current_site(request).domain
#         reset_url = reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
#         full_reset_url = f"http://{domain}{reset_url}"
        
#         send_mail(
#             subject="Password Reset Request",
#             message=f"Use the link below to reset your password: {full_reset_url}",
#             from_email="lastborn.ai@gmail.com",
#             recipient_list=[user.email],
#         )

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

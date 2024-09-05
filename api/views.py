from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    # PasswordResetSerializer, 
    UserSerializer, 
    MyTOPS, 
    RegistrationSerializer, 
    CarouselImageSerializer, 
    DisplayShowsSerializer, 
    UpcomingEventSerializer, 
    BlogSerializer
)
from .models import User, CarouselImage, HomeDisplayShows, UpcomingEvent, Blog


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTOPS

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protectedView(request):
    output = f"Welcome {request.user}, Authentication successful"
    return Response({"message": output}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        token_generator = PasswordResetTokenGenerator()
        if user is not None and token_generator.check_token(user, token):
            user.set_password(request.data['password'])
            user.save()
            return Response({"success": "Password has been reset."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)


# Carousel Image View
@api_view(['GET'])
def fashion_image_list(request):
    images = CarouselImage.objects.all()
    serializer = CarouselImageSerializer(images, many=True)
    return Response(serializer.data)


# API Routes
@api_view(['GET'])
def view_all_routes(request):
    data = [
        'api/token/refresh/',
        'api/register/',
        'api/token/',
        'api/userinfo/',
        'api/carousel-images/',
        'api/display-shows/',
        'api/upcoming-event/',
        'api/blog/',
        'api/password_reset/',
    ]
    return Response(data)


@api_view(['GET'])
def userInfo(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

# Home Page Display Shows View
@api_view(['GET'])
def display_show(request):
    images = HomeDisplayShows.objects.all()
    serializer = DisplayShowsSerializer(images, many=True)
    return Response(serializer.data)

# Upcoming Event View
@api_view(['GET'])
def upcoming_event(request):
    images = UpcomingEvent.objects.all()
    serializer = UpcomingEventSerializer(images, many=True)
    return Response(serializer.data)

# Blog Section View
@api_view(['GET'])
def blog_section(request):
    images = Blog.objects.all()
    serializer = BlogSerializer(images, many=True)
    return Response(serializer.data)

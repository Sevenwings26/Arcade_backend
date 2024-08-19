from .models import User, CarouselImage, HomeDisplayShows, UpcomingEvent, Blog
from .serializers import  UserSerializer, MyTOPS, RegistrationSerializer, CarouselImageSerializer, DisplayShowsSerializer, UpcomingEventSerializer, BlogSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status



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


# carousel
# Fashion Image View
@api_view(['GET'])
def fashion_image_list(request):
    """
    View to list all fashion images
    """
    images = CarouselImage.objects.all()
    serializer = CarouselImageSerializer(images, many=True)
    return Response(serializer.data)


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
    ]
    return Response(data)


@api_view(['GET'])
def userInfo(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

# HomePageDisplay
@api_view(['GET'])
def display_show(request):
    images = HomeDisplayShows.objects.all()
    serializer = DisplayShowsSerializer(images, many=True)
    return Response(serializer.data)

# UpcomingEvent
@api_view(['GET'])
def upcoming_event(request):
    images = UpcomingEvent.objects.all()
    serializer = UpcomingEventSerializer(images, many=True)
    return Response(serializer.data)

# blog section 
@api_view(['GET'])
def blog_section(request):
    images = Blog.objects.all()
    serializer = BlogSerializer(images, many=True)
    return Response(serializer.data)
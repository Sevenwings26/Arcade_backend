from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', views.RegisterView.as_view(), name="register-user"),
    path('user/', views.userInfo, name="userinfo"),
    path('test/', views.protectedView, name='test'),
    path('', views.view_all_routes, name='all-routes'),
    path('carousel-images/', views.fashion_image_list, name='carousel-images'),
    path('display-shows/', views.display_show, name='display-shows'),
    path('upcoming-event/', views.upcoming_event, name='event'),
    path('blog/', views.blog_section, name="blog"),

    # password-reset 
    # path('password-reset/', views.PasswordResetView.as_view(), name="password-reset"),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name="password-reset-confirm"),

]

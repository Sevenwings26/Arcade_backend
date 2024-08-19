from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(blank=False, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def profile(self):
        profile = Profile.objects.get(user = self)

# not important 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # detele profile by removing the user
    first_name = models.CharField(max_length=100)
    bio = models.TextField()
    profile_pic = models.ImageField('/profile_picture')
    verified = models.BooleanField(default=False)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
# Settled authentication
 

# Hero - section model 
class CarouselImage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='carousel_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HomeDisplayShows(models.Model):
    title = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='HomepageEvent_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class UpcomingEvent(models.Model):
    title = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to ='Upcoming_event/')


class Blog(models.Model):
    title = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='blog')
    description = models.CharField(max_length=300)
    body = models.TextField()

    def __str__(self):
        return f"Title of blog - {self.title}"
    
    
from django.contrib import admin
from .models import Profile, User, CarouselImage, HomeDisplayShows, UpcomingEvent, Blog


# Register your models here.
# iarowosola25@gmail.com
# arcade
# arcade123

# Create admin view for User model
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','first_name','email']

# Create admin view for Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'verified']
    list_editable = ['verified']

class CarouselAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CarouselImage, CarouselAdmin)
admin.site.register(HomeDisplayShows)
admin.site.register(UpcomingEvent)
admin.site.register(Blog)


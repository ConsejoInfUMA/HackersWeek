from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Venue)
admin.site.register(TimeStripe)
admin.site.register(Event)
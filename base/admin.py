from django.contrib import admin

# Register your models here.
from .models import Space, Topic, Message,User

admin.site.register(User)

admin.site.register(Space)
admin.site.register(Topic)
admin.site.register(Message)

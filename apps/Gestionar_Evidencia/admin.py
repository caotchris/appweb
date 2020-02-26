from django.contrib import admin
from .models import MyImage, MyVideo, MyAudio

admin.site.register(MyImage)
admin.site.register(MyVideo)
admin.site.register(MyAudio)

from django.contrib import admin
from .models import OtpRequest, CustomUser, Profile

admin.site.register(OtpRequest)
admin.site.register(CustomUser)
admin.site.register(Profile)
from django.urls import path
from .views import RequestOtp, VerifyOtp
urlpatterns = [
    path('request/', RequestOtp.as_view(), name='request_otp'),
    path('verify/', VerifyOtp.as_view(), name='verify_otp'),
]

from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from .serializers import RequestOtpSerializer, RequestotpResponseSerializer, VerifyOtpSerializer, VerifyOtpResponseSerializer
from .models import OtpRequest
import kavenegar
from django.conf import settings
import datetime


class OncePerMinuteThrottle(UserRateThrottle):
    rate = '1/minute'

class RequestOtp(APIView):
    throttle_classes = [OncePerMinuteThrottle,]


    def post(self, request):
        serializer = RequestOtpSerializer(data=request.data)
        if serializer.is_valid():
            req_otp = OtpRequest()
            req_otp.phone = serializer.validated_data['phone']
            req_otp.channel = serializer.validated_data['channel']
            req_otp.generate_password()
            req_otp.save()

            # api = kavenegar.KavenegarAPI(settings.SMS_API_KEY)
            # response = api.verify_lookup({
            #     'receptor': req_otp.phone,
            #     'token': req_otp.password,
            #     'template': settings.OTP_TEMPLATE,
            # })
            # print(response)
            return Response(RequestotpResponseSerializer(req_otp).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtp(APIView):
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            query = OtpRequest.objects.filter(
                request_id=serializer.validated_data['request_id'],
                phone=serializer.validated_data['phone'],
                password=serializer.validated_data['password'],
                valid_until__gte=datetime.datetime.now()
            )
            if query.exists():
                User = get_user_model()
                userq = User.objects.filter(username=serializer.validated_data['phone'])
                if userq.exists():
                    user = userq.first()
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(data=VerifyOtpResponseSerializer({
                        'token': token,
                        'new_user': False,
                    }).data)
                else:
                    user = User.objects.create(username=serializer.validated_data['phone'])
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(data=VerifyOtpResponseSerializer({
                        'token': token,
                        'new_user': True,
                    }).data)
            else:
                return Response(None, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

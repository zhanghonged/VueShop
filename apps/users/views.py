from django.shortcuts import render

# Create your views here.
import random
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import SmsSerializer, UserRegSerializer
from .models import VerifyCode
from apps.utils.yunpian import Yunpian
from VueShop.settings import APIKEY
User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def general_code(self):
        """
        生产四位数字的随机验证码
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(random.choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        """
        重新create方法
        """
        serializer = self.get_serializer(data=request.data)
        # is_valid 验证不过直接抛错，返回400错误
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        yun_pian = Yunpian(APIKEY)
        code = self.general_code()
        sms_status = yun_pian.send_sms(code=code ,mobile=mobile)
        if sms_status["code"] != 0:
            return Response({
                "mobile":sms_status["msg"]
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code,mobile=mobile)
            code_record.save()
            return Response({
                "mobile":mobile
            },status=status.HTTP_201_CREATED)

class UserViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

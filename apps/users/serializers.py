import re
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

from VueShop.settings import REGEX_MOBILE
from .models import VerifyCode
User = get_user_model()

class SmsSerializer(serializers.Serializer):

    mobile = serializers.CharField(max_length=11,min_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile: 手机号
        :return:
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已存在")
        # 验证手机号码是否规范
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不规范")
        # 验证发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile):
            raise serializers.ValidationError("距离上一次操作未超过60s")

        return mobile

class UserRegSerializer(serializers.ModelSerializer):
    # write_only=True 序列化得时候就不用序列号这个字段了，返回也没有这个字段了
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,label="验证码",
                                 error_messages= {
                                     "blank":"请输入验证码",
                                     "max_length":"验证码格式错误",
                                     "min_length": "验证码格式错误",
                                 })

    username = serializers.CharField(required=True, allow_blank=False, label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(),message="用户已存在")]
                                     )
    password = serializers.CharField(
        style={'input_type':'password'}, label="密码", write_only=True
    )

    def create(self, validated_data):
        """
        重载create函数，使密码入库加密
        """
        user = super(UserRegSerializer,self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validated_code(self, code):
        # 验证码是否存在
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_records = verify_records[0]
            # 验证码是否是5分钟之前的
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_records.add_time:
                raise serializers.ValidationError("验证码已过期")
            if last_records.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        """
        :param attrs: validate后返回的一个总的dict
        :return:
        """
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")
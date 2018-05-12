import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.models import Goods
from VueShop.settings import REGEX_MOBILE

class GoodsBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ("id","name","category")

class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsBriefSerializer()
    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields = ("user", "goods"),
                message = "已经收藏"
                )
        ]

        fields = ("user", "goods", "id")

class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserLeavingMessage
        fields = ("id","user","message_type","subject","message","file","add_time")

class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    signer_mobile = serializers.CharField(max_length=11)

    #验证手机号码是否合法
    def validate_signer_mobile(self,signer_mobile):
        if not re.match(REGEX_MOBILE,signer_mobile):
            raise serializers.ValidationError("手机号码不规范")
        return signer_mobile

    class Meta:
        model = UserAddress
        fields = ("id","user","province","city","district","address","signer_name","signer_mobile","add_time")
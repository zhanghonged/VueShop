# -*- coding: utf-8 -*-
import time
from random import Random
from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart, OrderInfo
from goods.serializers import GoodsSerializer

class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)
    class Meta:
        model = ShoppingCart
        fields = ("goods","nums")

class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量",min_value=1,
                                    error_messages={
                                        "min_value":"商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        #修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    def generate_order_sn(self):
        # 当前时间+userid+随机数
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
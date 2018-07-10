from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializer import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
from utils.permissions import IsOwnerOrReadOnly
# Create your views here.

class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已收藏
    create:
        收藏商品
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # 重载 CreateModelMixin 的 perform_create 方法，实现用户收藏后，商品收藏数增加逻辑
    def perform_create(self, serializer):
        instance = serializer.save()
        # 通过这个instance Userfav找到goods
        goods = instance.goods
        goods.fav_num +=1
        goods.save()

    # 重载 DestroyModelMixin 的 perform_destroy 方法，实现用户取消收藏后，商品收藏数减1逻辑
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()
        # delete后就取不到goods了
        instance.delete()


class LeavingMessageViewset(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    用户留言
    list:
        用户留言列表
    create:
        添加留言
    delete:
        删除留言
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    #用户只能看到自己留言
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)

class AddressViewset(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    retrieve:
        收货地址详细
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


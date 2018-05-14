from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
# Create your views here.

class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        删除购物记录
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewset(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create：
        新增订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)

        #根据购物车的商品计算订单价格
        order_mount = 0
        for shop_cart in shop_carts:
            order_mount += shop_cart.goods.shop_price*shop_cart.nums
        serializer.validated_data["order_mount"] = order_mount
        order = serializer.save()
        #添加订单商品表添加数据，并清空购物车
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order


from datetime import datetime
from django.shortcuts import redirect

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView, Response

from utils.permissions import IsOwnerOrReadOnly
from utils.alipay import AliPay
from .serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from VueShop.settings import private_key_path, ali_pub_key_path
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

class AliPayView(APIView):
    """
    """
    def get(self,request):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)
        alipay = AliPay(
            appid="2016091500517899",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:

            # order_sn = processed_dict.get("out_trade_no", None)
            # trade_no = processed_dict.get("trade_no", None)
            # trade_status = processed_dict.get("trade_status", None)
            #
            # existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            # for existed_order in existed_orders:
            #     existed_order.pay_status = trade_status
            #     existed_order.trade_no = trade_no
            #     existed_order.pay_time = datetime.now()

            response = redirect("index")
            response.set_cookie("nextPath","pay",max_age=2)
            return response
        else:
            response = redirect("index")
            return response

    def post(self,request):
        """
        处理支付宝的notify_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key ,value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign",None)
        alipay = AliPay(
            appid="2016091500517899",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get("out_trade_no", None)
            trade_no = processed_dict.get("trade_no", None)
            trade_status = processed_dict.get("trade_status", None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()

            return Response("success")

from rest_framework import mixins
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle

from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer
from .filters import GoodsFilter
# Create your views here.
class GoodstPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

class GoodsListViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页,分页、过滤、搜索、排序
    """


    # throttle_classes = (AnonRateThrottle,UserRateThrottle)

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodstPagination
    #authentication_classes = (TokenAuthentication, )

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    filter_class = GoodsFilter
    search_fields = ('=name', 'goods_brief','goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    # 重载 RetrieveModelMixin 的 retrieve 方法，实现商品点击数增加逻辑
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer

class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    首页轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer




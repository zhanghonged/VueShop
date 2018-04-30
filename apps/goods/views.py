from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets

from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer, CategorySerializer
from .filters import GoodsFilter
# Create your views here.
class GoodstPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100

class GoodsListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表页,分页、过滤、搜索、排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    pagination_class = GoodstPagination


    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    filter_class = GoodsFilter
    search_fields = ('=name', 'goods_brief','goods_desc')
    ordering_fields = ('name','sold_num', 'add_time')

class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer


















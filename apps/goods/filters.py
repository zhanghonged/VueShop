#coding:utf-8

from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(filters.FilterSet):
    """
    商品的过滤类
    """
    pricemin = filters.NumberFilter(name='shop_price',lookup_expr='gt')
    pricemax = filters.NumberFilter(name='shop_price',lookup_expr='lt')
    top_category = filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max']
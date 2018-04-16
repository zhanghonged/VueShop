#coding:utf-8
from django.views.generic.base import View
from goods.models import Goods

class GoodsListView(View):
    def get(self, request):
        """
        通过django的view实现商品列表页
        :param request:
        :return:
        """
        goods = Goods.objects.all()[:10]

        from django.core import serializers
        import json
        json_data = serializers.serialize("json",goods)
        json_data = json.loads(json_data)

        from django.http import HttpResponse, JsonResponse
        return JsonResponse(json_data, safe=False)